"""
Tests the backend module

"""

from fbml.model import Node, Method
from fbml.value import INTEGERS, singleton

from fbml import backend



def test_increment():
    """
    Test the output of::

        method increment
            a : Z
        procedure
            c = a + 1;
        end c

    """
    node_c = Node('add', {'a': Node('a', {}), 'b': Node('b', {}) })
    method = Method('increment', {'a': INTEGERS}, {'b': singleton(1)}, node_c)

    compiler = backend.LLVMBackend(backend.METHODS)
    print(compiler.compile_function(method.name , ['a'], [method]))
    assert False


def test_abs():
    """
    Test the output of::

        method abs
            a < 0, a : Z
        procedure
            b = -a;
        end b

        method abs
            a >= 0, a : Z
        procedure
        end a

    """
    node_b = Node('neg', {'a': Node('a', {}) })
    abs_minus = Method('abs',
            {'a': INTEGERS},
            {},
            node_b)

    node_b = Node('a', {})
    abs_plus = Method('abs',
            {'a': INTEGERS},
            {},
            node_b)


    compiler = backend.LLVMBackend(backend.METHODS)
    print(compiler.compile_function('abs' , ['a'], [abs_minus, abs_plus]))
    assert False

