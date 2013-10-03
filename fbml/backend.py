"""
.. currentmodule:: fbml.backend
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

A simple backend written in llvm

"""
from copy import copy
from functools import reduce
from itertools import starmap
from operator import itemgetter
import collections
import llvm
import llvm.core as llvmc

import logging
L = logging.getLogger(__name__)

from fbml import value

TYPE_MAP = {
    'Integer'  : (llvmc.Type.int(),'int'),
    'Real'     : (llvmc.Type.double(),'real'),
    'Boolean'  : (llvmc.Type.int(1),'int'),
}

BUILDIN_MAP = {
    'add'      : 'add',
    'sub'      : 'sub',
    'mul'      : 'mul',
    'and'      : 'and_',
    'neg'      : 'neg',
    'ilt'      : llvmc.ICMP_SLT,
    'igt'      : llvmc.ICMP_SGT,
    'ile'      : llvmc.ICMP_SLE,
    'ige'      : llvmc.ICMP_SGE,
    'ieq'      : llvmc.ICMP_EQ,
}

INTEGER_CMP = {
        llvmc.ICMP_SLT,
        llvmc.ICMP_SGT,
        llvmc.ICMP_SLE,
        llvmc.ICMP_SGE,
        llvmc.ICMP_EQ,
        }


def constant_from_value(val):
    """
    :param val:
        The value

    :returns: an llvm constant
    """
    llvm_type, type_name = TYPE_MAP[typename_of_value(val)]
    return getattr(llvmc.Constant, type_name)(llvm_type, val)

def type_of_value(val):
    """
    :param val:
        The value or value set

    :returns:
        an llvm type
    """
    return TYPE_MAP[typename_of_value(val)][0]

def typename_of_value(val):
    """
    :param val:
        a value or a value set

    :returns: the typename of a value
    """
    if isinstance(val, bool):
        typename = 'Boolean'
    elif isinstance(val, int):
        typename = 'Integer'
    else:
        typename = 'Integer'
        L.warning('Called typename_of_value on %s, returns "%s"', val, typename)
    return typename

def order_arguments(arguments):
    """
    requires a strict alphabetical order of arguments
    """
    return list(sorted(arguments.items(), key=itemgetter(0)))

def buildin_method(bldr, name, args):
    """
    calls an build in method
    """
    if name in BUILDIN_MAP:
        func = BUILDIN_MAP[name]
        if func in INTEGER_CMP:
            lhs, rhs = args
            assert args[0].type == args[1].type
            return bldr.icmp(func, lhs, rhs)
        else:
            try:
                lhs, rhs = args
                assert lhs.type == rhs.type
            except ValueError: pass
            return getattr(bldr, BUILDIN_MAP[name])(*args)

    elif name in TYPE_MAP:
        test = args[0].type == TYPE_MAP[name][0]
        ret = constant_from_value(test)
        return ret
    else:
        raise RuntimeError("{name} is not a buildin function".format(name=name))

Result = collections.namedtuple('Result', [
    'data',
    'bldr',
    ])

Block = collections.namedtuple('Block', [
    'context',
    'method',
    ])


class LLVMCompiler (collections.namedtuple('Context', [
    'datamap',
    'backend',
    'bldr',
    ])):

    """
    Context is an immutable class used when compiling
    """

    def __copy__(self):
        return self._replace(datamap=self.datamap.copy())

    def copy(self):
        return self.__copy__()

    def update_datamap(self, dictlike):
        """
        :returns:
            a new context with an updated datamap
        """
        copy = self.copy()
        copy.datamap.update(dictlike)
        return copy

    def with_builder(self, builder):
        """
        :returns:
            a new context with an updated builder
        """
        return self._replace(bldr=builder)

    def _create_blocks(self, methods, results=tuple()):
        """
        creates a tuples of blocks
        """
        bldr = self.bldr
        method, *rest = methods
        if rest:

            function = bldr.basic_block.function

            succ = function.append_basic_block('succ.' + str(len(rest)))
            fail = function.append_basic_block('fail.' + str(len(rest)))

            internal = self.update_datamap(
                    (name, constant_from_value(val))
                    for name, val in method.constants.items()
                    )

            result = internal.compile_program_graph(method.contraint)

            bldr.cbranch(result.data, succ, fail)

            succ_context = self.with_builder(llvmc.Builder.new(succ))
            fail_context = self.with_builder(llvmc.Builder.new(fail))

            return fail_context._create_blocks(rest,
                    results + ( Block(succ_context, method), )
                    )
        else:
            return results + ( Block(self, method), )

    @staticmethod
    def _join_blocks(results):
        """
        Joins the results from the blocks
        """
        succ_result, *rest = results
        if rest:
            fail_result = LLVMCompiler._join_blocks(rest)

            function = succ_result.bldr.basic_block.function

            merge = function.append_basic_block(
                     'merg.' + str(len(rest)))

            fail_result.bldr.branch(merge)
            succ_result.bldr.branch(merge)

            bldr = llvmc.Builder.new(merge)

            phi = bldr.phi(succ_result.data.type)
            phi.add_incoming(fail_result.data, fail_result.bldr.basic_block)
            phi.add_incoming(succ_result.data, succ_result.bldr.basic_block)

            return Result(phi, bldr)
        else:
            return succ_result

    def compile_methods(self, methods):
        """
        Compiles an list of methods
        _"""

        blocks = self._create_blocks(methods)
        results = [compiler.compile_method(method)
                    for compiler, method in blocks]
        return self._join_blocks(results)

    def compile_method(self, method):
        """
        Compiles a method

        :param self:

            The self.data **must** at least contain the name of the
            arguments

        :returns: a return tuple
        """
        internal = self.update_datamap(
                (name, constant_from_value(val))
                for name, val in method.constants.items()
                )
        if method.is_buildin():
            return internal.compile_buildin_method(method)
        else:
            return internal.compile_program_graph(method.target)

    def compile_program_graph(self, basenode):
        internal = self.copy()

        def reduce_opr(compiler, node):
            """ reduces the outputs of a compile function """
            result = compiler.compile_node(node)
            internal = compiler.copy().with_builder(result.bldr)
            internal.datamap[node] = result.data
            return internal

        internal = reduce(reduce_opr,
                reversed(basenode.nodes_in_order()),
                self)
        return Result(internal.datamap[basenode], internal.bldr)


    def compile_node(self, node):
        if not node.sources:
            try:
                return Result(self.datamap[node.name], self.bldr)
            except KeyError:
                raise RuntimeError('Could not copile node, because {name}'
                        ' where not computed in {datamap}'.format(
                            name = node.name, datamap = self.datamap))
        else:
            return self.compile_function_call(node)

    def compile_buildin_method(self, method):
        arg_val = [self.datamap[name] for name in sorted(method.arguments)]
        return Result(
                buildin_method(self.bldr, method.target, arg_val),
                self.bldr
                )

    def compile_function_call(self, node):
        internal = self.update_datamap(
                (name, self.datamap[node])
                for name, node in node.sources.items()
                )

        methods = node.methods
        if not methods:
            raise RuntimeError('No methods, consider linking')
        elif len(methods) == 1:
            # Inline function
            method, = methods
            return internal.compile_method(method)
        else:
            arg_val = [internal.datamap[node] for name, node in
                        order_arguments(node.sources)]
            func = self.backend.function_from_methods(methods)
            node_data = internal.bldr.call(
                    func,
                    arg_val)
            return Result(node_data, internal.bldr)

class LLVMBackend(object):
    """
    This is the LLVM backend for fbml
    """

    def __init__(self):
        self.module = llvmc.Module.new('sandbox')
        self.functions = {}

    def build_function(self, name, argument_names, methods):
        """
        Creates a LLVM function from all of these methods. Assumes that the
        methods have the same argument names.
        """

        allowed_args = [method.allowed_arguments(value.union)
                for method in methods]

        arguments = {a:
                reduce(value.union,(allowed[a] for allowed in allowed_args))
                     for a in argument_names}

        sorted_args = order_arguments(arguments)

        return_values = reduce(value.union,
                (method.predict_return() for method in methods))

        arg_types = [type_of_value(arg) for name, arg in sorted_args]

        function = llvmc.Function.new(
            self.module,
            llvmc.Type.function(
                type_of_value(return_values),
                arg_types
                ),
            name
            )
        self.functions[tuple(methods)] = function

        entry = function.append_basic_block('entry')
        bldr = llvmc.Builder.new(entry)

        values = {}
        for arg, llvm_arg in zip(sorted_args, function.args):
            name, _ = arg
            llvm_arg.name = name
            values[name] = llvm_arg

        result = LLVMCompiler(values, self, bldr).compile_methods(methods)
        result.bldr.ret(result.data)
        try:
            function.verify()
        except llvm.LLVMException as exc:
            L.error(eval(str(exc)).decode(encoding='UTF-8'))
        return function

    def function_from_methods(self, methods):
        """
        get_function
        """
        key = tuple(methods)
        if key in self.functions:
            return self.functions[key]
        else:
            first, *_ = methods
            name = first.name
            argument_names = list(first.arguments)
            return self.build_function(name, argument_names, methods)


