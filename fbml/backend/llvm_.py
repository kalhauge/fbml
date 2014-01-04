"""
.. currentmodule:: fbml.backend
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

A simple backend written in llvm

"""
#pylint: disable = E1101
from functools import reduce
from operator import itemgetter
import collections
import llvm
import llvm.core as llvmc

import logging
L = logging.getLogger(__name__)

from fbml.analysis import typeset

BUILDIN_MAP = {
    'r_add': 'fadd',
    'r_sub': 'fsub',
    'r_mul': 'fmul',
    'r_neg': 'fneg',
    'r_div': 'fdiv',

    'r_lt':  llvmc.FCMP_ULT,
    'r_gt':  llvmc.FCMP_UGT,
    'r_le':  llvmc.FCMP_ULE,
    'r_ge':  llvmc.FCMP_UGE,
    'r_eq':  llvmc.FCMP_UEQ,

    'i_add': 'add',
    'i_sub': 'sub',
    'i_mul': 'mul',
    'i_neg': 'neg',

    'i_lt':  llvmc.ICMP_SLT,
    'i_gt':  llvmc.ICMP_SGT,
    'i_le':  llvmc.ICMP_SLE,
    'i_ge':  llvmc.ICMP_SGE,
    'i_eq':  llvmc.ICMP_EQ,

    'and':   'and_',
}

REAL_MAP = {}

INTEGER_CMP = {
    llvmc.ICMP_SLT,
    llvmc.ICMP_SGT,
    llvmc.ICMP_SLE,
    llvmc.ICMP_SGE,
    llvmc.ICMP_EQ,
}

REAL_CMP = {
    llvmc.FCMP_ULT,
    llvmc.FCMP_UGT,
    llvmc.FCMP_ULE,
    llvmc.FCMP_UGE,
    llvmc.FCMP_UEQ,
}


def buildin_method(bldr, name, args):
    """
    calls an build in method
    """
    if name == 'load':
        return args
    if name in BUILDIN_MAP:

        # TESTS
        if name.startswith('i'):
            assert args[0].type == TYPE_MAP['Integer'].internal
        elif name.startswith('r'):
            assert args[0].type == TYPE_MAP['Real'].internal
        else:
            pass

        funcname = BUILDIN_MAP[name]
        try:
            lhs, rhs = args
            print(lhs, rhs, args)
        except ValueError:
            arg, = args
            return getattr(bldr, funcname)(arg)
        else:
            assert lhs.type == rhs.type
            if funcname in INTEGER_CMP:
                return bldr.icmp(funcname, lhs, rhs)
            elif funcname in REAL_CMP:
                assert False, 'Real comparation'
                return bldr.fcmp(funcname, lhs, rhs)
            else:
                assert not funcname.startswith('f'), "{}({}, {})".format(
                    funcname, lhs, rhs
                )
                return getattr(bldr, funcname)(lhs, rhs)

#    elif name in TYPE_MAP:
#        test = args[0].type == TYPE_MAP[name][0]
#        ret = constant_from_value(test)
#        return ret
    else:
        raise RuntimeError('Not a buildin method %s' % name)


TYPE_MAP = {
    'Integer': (llvmc.Type.int(), 'int'),
    'Real':    (llvmc.Type.double(), 'real'),
    'Boolean': (llvmc.Type.int(1), 'int'),
}


def constant_from_value(valueset):
    """
    :param val:
        The value

    :returns: an llvm constant
    """
    val, = valueset
    llvm_type, type_name = TYPE_MAP[typename_of_value(val)]
    return getattr(llvmc.Constant, type_name)(llvm_type, val)


def type_of_value(valueset):
    """
    :param valueset:
        a valueset

    :returns:
        an llvm type
    """
    val, = valueset
    return TYPE_MAP[val][0]


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
        L.warning(
            'Called typename_of_value on %s, returns "%s"',
            val, typename
        )
    return typename


def order_arguments(arguments):
    """
    requires a strict alphabetical order of arguments
    """
    return list(sorted(arguments.items(), key=itemgetter(0)))

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
    'functions',
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
        method, rest = methods[0], methods[1:]
        if rest:

            function = bldr.basic_block.function

            succ = function.append_basic_block('succ.' + str(len(rest)))
            fail = function.append_basic_block('fail.' + str(len(rest)))

            result = self.compile_program_graph(method.guard)

            bldr.cbranch(result.data, succ, fail)

            succ_context = self.with_builder(llvmc.Builder.new(succ))
            fail_context = self.with_builder(llvmc.Builder.new(fail))

            return fail_context._create_blocks(
                rest, results + (Block(succ_context, method),)
            )
        else:
            return results + (Block(self, method), )

    @staticmethod
    def _join_blocks(results):
        """
        Joins the results from the blocks
        """
        succ_result, rest = results[0], results[1:]
        if rest:
            fail_result = LLVMCompiler._join_blocks(rest)

            function = succ_result.bldr.basic_block.function

            merge = function.append_basic_block('merg.' + str(len(rest)))

            fail_result.bldr.branch(merge)
            succ_result.bldr.branch(merge)

            bldr = llvmc.Builder.new(merge)

            phi = bldr.phi(succ_result.data.type)
            phi.add_incoming(fail_result.data, fail_result.bldr.basic_block)
            phi.add_incoming(succ_result.data, succ_result.bldr.basic_block)

            return Result(phi, bldr)
        else:
            return succ_result

    def compile_method(self, method):
        """
        Compiles a method

        :param self:

            The self.data **must** at least contain the name of the
            arguments

        :returns: a return tuple
        """

        if method.is_buildin:
            return self.compile_buildin_method(method)
        else:
            return self.compile_program_graph(method.statement)

    def compile_program_graph(self, basenode):
        internal = self.copy()

        def reduce_opr(compiler, node):
            """ reduces the outputs of a compile function """
            result = compiler.compile_node(node)
            internal = compiler.copy().with_builder(result.bldr)
            internal.datamap[node] = result.data
            return internal

        internal = reduce(
            reduce_opr,
            reversed(basenode.nodes_in_order()), self
        )
        return Result(internal.datamap[basenode], internal.bldr)

    def compile_node(self, node):
        if not node.sources:
            try:
                return Result(self.datamap[node.name], self.bldr)
            except KeyError:
                raise RuntimeError(
                    'Could not copile node, because {name}'
                    ' where not computed in {datamap}'.format(
                        name=node.name, datamap=self.datamap
                    ))
        else:
            return self.compile_function_call(node)

    def compile_buildin_method(self, method):
        return Result(
            buildin_method(
                self.bldr, method.code,
                [self.datamap[arg] for arg in method.argmap]
            ),
            self.bldr
        )

    def compile_function_call(self, node):
        if len(node.function.methods) == 1:
            # Inline function
            internal = self.update_datamap(
                (argname, self.datamap[node]) for argname, node in
                zip(node.function.arguments, node.sources)
            )
            method, = node.function.methods
            return internal.compile_method(method)
        else:
            arg_val = [self.datamap[n] for n in node.sources]
            func = self.functions[node]
            node_data = self.bldr.call(func, arg_val)
            return Result(node_data, self.bldr)

    def compile_function(self, function):
        """ Compiles a function """
        blocks = self._create_blocks(function.methods)
        results = [
            compiler.compile_method(method) for compiler, method in blocks
        ]
        return self._join_blocks(results)


from collections import namedtuple
LLVMType = namedtuple('LLVMType', ('internal', 'name', 'char'))

LLVM_TYPE_MAP = {
    'Integer':   LLVMType(llvmc.Type.int(), 'int', 'i'),
    'Real':      LLVMType(llvmc.Type.double(), 'real', 'r'),
    'Boolean':   LLVMType(llvmc.Type.int(1), 'int', 'b')
}


def llvm_type(type_set):
    """ Given a type_set with only one ellement this function will
        reuturn the llvm type """
    type_, = type_set
    return LLVM_TYPE_MAP[type_]


def llvm_const(value):
    """ """
    type_ = llvm_type(typeset.const(value))
    return getattr(llvmc.Constant, type_.name)(type_.internal, value)


def initial_values(function, llvm_function):
    values = {}
    for name, llvm_arg in zip(function.arguments, llvm_function.args):
        llvm_arg.name = name
        values[name] = llvm_arg

    values.update(
        (name, llvm_const(value)) for name, value in function.constants.items()
    )

    return values


class LLVMBackend(object):
    """
    This is the LLVM backend for fbml
    """

    def __init__(self):
        self.module = llvmc.Module.new('sandbox')
        self.functions = {}

    def build_function(self, function, types):
        """
        Creates a LLVM function from all of these methods. Assumes that the
        methods have the same argument names.
        """
        return_type = function.evaluate(typeset, types)
        if not return_type:
            raise Exception(
                'Function not valid for arguments',
                function, types
            )

        build_functions = {
            node: self.build_function(depfunc, deptypes)
            for node, (depfunc, deptypes) in evaluator.depends.items()
            if depfunc != function and len(depfunc.methods) > 1
        }

        arg_types = [llvm_type(arg).internal for arg in types]
        return_type = llvm_type(return_type).internal

        func_type = llvmc.Type.function(return_type, arg_types)
        func_name = \
            function.name + '_' + ''.join(llvm_type(arg).char for arg in types)

        L.debug("Building: %s %s", func_name, func_type)

        llvm_function = llvmc.Function.new(self.module, func_type, func_name)

        self.functions[(function, types)] = llvm_function
        values = initial_values(function, llvm_function)

        L.debug("Assigned Variables %s", values)

        entry = llvm_function.append_basic_block('entry')
        bldr = llvmc.Builder.new(entry)

        compiler = LLVMCompiler(values, build_functions, bldr)
        compiler.compile_function(function)

        try:
            llvm_function.verify()
        except llvm.LLVMException as exc:
            L.error(eval(str(exc)).decode(encoding='UTF-8'))

        return llvm_function

    def compile(self, function, types):
        """ Compiles a FBML function to a LLVM Function """
        type_id = tuple(
            type_ for name, type_ in sorted(types.items(), key=itemgetter(1))
        )
        key = (function, type_id)
        if key in self.functions:
            return self.functions[key]
        else:
            return self.build_function(function, types)
