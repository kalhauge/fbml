"""
.. currentmodule:: fbml.backend
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

A simple backend written in llvm

"""
from functools import reduce
from operator import itemgetter
import collections
import llvm.core as llvmc

import logging
L = logging.getLogger(__name__)

from fbml import value
from fbml import model


BlockData = collections.namedtuple('Block', [
    'values',
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
            {'a': value.INTEGERS}, {}, 'sub')
        ],
}


class LLVMBackend(object):
    """
    This is the LLVM backend for fbml
    """

    def __init__(self, methods):
        self.module = llvmc.Module.new('sandbox')
        self.methods = methods
        self.functions = {}

    def compile_constraint(self, arguments, values, bldr):
        """
        compiles the constraint of a branch, returns a true block
        """
        return llvm_constant('Boolean', True)

    def compile_function(self, name, argument_names, methods):
        """
        Creates a LLVM function from all of these methods. Assumes that the
        methods have the same argument names.
        """
        arguments = {a: reduce(value.union,
                    ( method.arguments[a] for method in methods ))
                    for a in argument_names}

        sorted_args = list(sorted(arguments.items(), key= itemgetter(0)))

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

        bldr, val = self.compile_methods(methods, return_values, values, bldr)

        bldr.ret(val)
        try:
            self.module.verify()
        except Exception as e:
            print(eval(str(e)).decode(encoding='UTF-8'))
        return function

    def compile_methods(self, methods, ret_vals, values, bldr):
        head, *tail = methods
        if tail:
            func = bldr.basic_block.function

            true_block = func.append_basic_block('true-' + str(head))
            false_block = func.append_basic_block('false-' + str(head))

            condition = self.compile_constraint(head.arguments,
                    values, bldr)
            bldr.cbranch(condition, true_block, false_block)

            true_bldr, val_true = self.compile_method(head,
                    values,
                    llvmc.Builder.new(true_block))

            false_bldr, val_false = self.compile_methods(tail,
                    ret_vals,
                    values,
                    llvmc.Builder.new(false_block))


            merge_block = func.append_basic_block('merge-' + str(head))
            true_bldr.branch(merge_block)
            false_bldr.branch(merge_block)

            m_bldr = llvmc.Builder.new(merge_block)
            phi = m_bldr.phi(llvm_type_of_value_set(ret_vals))
            phi.add_incoming(val_true, true_block)
            phi.add_incoming(val_false, false_bldr.basic_block)
            return m_bldr, phi

        else:
            return self.compile_method(head, values, bldr)


    def compile_method(self, method, values, bldr):
        """
        Compiles a method on block
        """
        nodes = list(reversed(method.target.nodes_in_order()))
        method_values = {}
        for node in nodes:
            print(node, method_values)
            if not node.sources:
                # Argument or constant.
                try:
                    consts = method.constants[node.name]
                except KeyError:
                    # argument
                    val = values[node.name]
                else:
                    val = self.create_constant_from_values(consts)
            else:
                methods = self.methods[node.name]
                if len(methods) == 1:
                    #inline, no recursion allowed on none spliting
                    #functions
                    function, = methods
                    if isinstance(function.target, str):
                        #buildin
                        val = getattr(bldr, function.target)(
                                *[method_values[node] for name, node in
                            sorted(node.sources.items(),key=itemgetter(0))],
                                name=str(node))
                else:
                    raise Exception()
            method_values[node] = val
        return bldr, method_values[method.target]

    def create_constant_from_values(self, consts):
        val, = consts
        return llvm_constant(type_of_value_set(consts), val)


