"""
.. currentmodule:: fbml.backend
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

A simple backend written in llvm

"""
from functools import reduce
from operator import itemgetter
import collections
import llvm
import llvm.core as llvmc

import logging
L = logging.getLogger(__name__)

from fbml import value
from fbml import model


CompileContext = collections.namedtuple('CompileContext', [
    'data',
    'bldr',
    ])

TYPE_MAP = {
    'Integer'  : (llvmc.Type.int(),'int'),
    'Real'     : (llvmc.Type.double(),'real'),
    'Boolean'  : (llvmc.Type.int(1),'int'),
}

def llvm_constant(name, val):
    llvm_type, type_name = TYPE_MAP[name]
    return getattr(llvmc.Constant, type_name)(llvm_type, val)

def type_of_value_set(value_set):
    return 'Integer'

def llvm_type_of_value_set(value_set):
    return TYPE_MAP[type_of_value_set(value_set)][0]

METHODS = {
    'add' : [
        model.Method('add',
            {'a': value.INTEGERS, 'b': value.INTEGERS}, {}, 'add')
        ],
    'neg' : [
        model.Method('add',
            {'a': value.INTEGERS}, {}, 'neg')
        ],
    'sub' : [
        model.Method('sub',
            {'a': value.INTEGERS, 'b': value.INTEGERS}, {}, 'sub')
        ],
}


def order_arguments(arguments):
    """
    requires a strict alpha betical order of arguments
    """
    return list(sorted(arguments.items(), key=itemgetter(0)))

def copy_context(context):
    """
    copies the context
    """
    return CompileContext(context.data.copy(), context.bldr)

class LLVMBackend(object):
    """
    This is the LLVM backend for fbml
    """

    def __init__(self, methods):
        self.module = llvmc.Module.new('sandbox')
        self.methods = methods
        self.functions = {}

    def compile_constraint(self, arguments, context):
        """
        compiles the constraint of a branch, returns a true block
        """
        return llvm_constant('Boolean', True), context.bldr

    def build_function(self, name, argument_names, methods):
        """
        Creates a LLVM function from all of these methods. Assumes that the
        methods have the same argument names.
        """
        arguments = {a: reduce(value.union,
                    ( method.arguments[a] for method in methods ))
                    for a in argument_names}

        sorted_args = order_arguments(arguments)

        return_values = reduce(value.union,
                (method.predict_value() for method in methods))

        arg_types = [llvm_type_of_value_set(arg) for name, arg in sorted_args]

        function = llvmc.Function.new(
            self.module,
            llvmc.Type.function(
                llvm_type_of_value_set(return_values),
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

        val, bldr = self.compile_methods(methods, return_values,
                CompileContext(values, bldr))

        bldr.ret(val)
        try:
            function.verify()
        except llvm.LLVMException as exc:
            L.error(eval(str(exc)).decode(encoding='UTF-8'))
        return function

    def compile_methods(self, methods, ret_vals, context):
        """
        Compiles methods
        """
        #TODO: REFACTOR
        head, *tail = methods
        if tail:
            func = context.bldr.basic_block.function

            true_block = func.append_basic_block('true-' + str(head))
            false_block = func.append_basic_block('false-' + str(head))

            condition, bldr = self.compile_constraint(head.arguments, context)
            bldr.cbranch(condition, true_block, false_block)

            true_context = CompileContext(
                    context.data, llvmc.Builder.new(true_block))
            true_data, true_bldr = self.compile_method(head, true_context)

            false_context = CompileContext(
                    context.data, llvmc.Builder.new(false_block))
            false_data, false_bldr = self.compile_methods(
                    tail, ret_vals, false_context)


            merge_block = func.append_basic_block('merge-' + str(head))
            true_bldr.branch(merge_block)
            false_bldr.branch(merge_block)

            print(true_data, false_data)
            m_bldr = llvmc.Builder.new(merge_block)
            phi = m_bldr.phi(llvm_type_of_value_set(ret_vals))
            phi.add_incoming(true_data, true_block)
            phi.add_incoming(false_data, false_bldr.basic_block)
            return phi, m_bldr
        else:
            return self.compile_method(head, context)


    def compile_method(self, method, context):
        """
        Compiles a method using a context

        :param context:

            The context.data **must** at least contain the name of the
            arguments

        :returns: the updated context.
        """
        L.debug('Compiles Method: %s %s', method, context)
        internal = copy_context(context)
        internal.data.update(
                (name, self.create_constant_from_values(val))
                for name, val in method.constants.items()
                )

        if isinstance(method.target, str):
            return self.compile_buildin_method(method, internal)
        else:
            return self.compile_program_graph(method.target, internal)

    def compile_buildin_method(self, method, context):
        """
        Buildin data
        """
        arguments = [context.data[name] for name in method.arguments]
        function = getattr(context.bldr, method.target)
        return function(*arguments, name=str(method)), context.bldr

    def compile_program_graph(self, node, context):
        """
        Compiles a program_graph, uses a node
        """
        def reduce_opr(context, node):
            """ reduces the outputs of a compile function """
            result, bldr = self.compile_node(node, context)
            internal = CompileContext(context.data, bldr)
            internal.data[node] = result
            return internal
        internal = reduce(reduce_opr, reversed(node.nodes_in_order()), context)
        return internal.data[node], internal.bldr

    def compile_node(self, node, context):
        if not node.sources:
            return context.data[node.name], context.bldr
        else:
            return self.compile_function_call(node, context)

    def compile_function_call(self, node, context):
        internal = copy_context(context)
        internal.data.update(
                (name, context.data[node])
                for name, node in node.sources.items()
                )
        L.debug("Compiles function call %s, %s, %s", node, context, internal.bldr)
        methods = self.methods[node.name]
        if len(methods) == 1:
            # Inline function
            method, = methods
            return self.compile_method(method, internal)
        else:
            arg_val = [internal.data[node] for name, node in
                        order_arguments(node.sources)]
            func = self.function_from_methods(methods)
            node_data = internal.bldr.call(
                    func,
                    arg_val,
                    name=str(node))
            return node_data, internal.bldr

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

    def create_constant_from_values(self, consts):
        val, = consts
        return llvm_constant(type_of_value_set(consts), val)


