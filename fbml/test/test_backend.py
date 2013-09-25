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
    print(compiler.build_function(method.name , ['a'], [method]))
    # assert False


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
    print(compiler.build_function('abs' , ['a'], [abs_minus, abs_plus]))
    #assert False

def test_clamp():
    """
    Test the output of::

        method clamp
            a <= high, a >= low, a : Z, high : Z, low : Z
        procedure
        end a

        method clamp
            a > high, a : Z, high : Z, low : Z
        procedure
        end high

        method clamp
            a < low, a : Z, high : Z, low : Z
        procedure
        end low

    """
    clamp_middle = Method('clamp',
            {'a': INTEGERS,
             'high' : INTEGERS,
             'low'  : INTEGERS },
            {},
            Node('a', {})
            )
    clamp_high = Method('clamp',
            {'a': INTEGERS,
             'high' : INTEGERS,
             'low'  : INTEGERS },
            {},
            Node('high', {})
            )

    clamp_low = Method('clamp',
            {'a': INTEGERS,
             'high' : INTEGERS,
             'low'  : INTEGERS },
            {},
            Node('low', {}))

    compiler = backend.LLVMBackend(backend.METHODS)
    print(compiler.build_function('clamp',
        ['a', 'high', 'low'],
        [clamp_middle, clamp_high, clamp_low]))
    #assert False

FACTORIAL = {
        'factorial' : [
            Method('factorial',
                {'a': singleton(1)}, {},
                Node('a', {})
            ),
            Method('factorial',
                {'a': INTEGERS}, {'c': singleton(1)},
                Node('factorial', {
                    'a': Node('sub', {
                            'a' : Node('a', {}),
                            'b' : Node('c', {})
                        })
                    })
                )
            ]
        }

def test_factorial():
    """
    Test the output of::

        method factorial
            a : {1}
        procedure
        end a

        method factorial
            a > 1, a : Z
        procedure
            b = factorial(a - 1) * a
        end b

    """
    methods = backend.METHODS.copy()
    methods.update(FACTORIAL)
    compiler = backend.LLVMBackend(methods)
    print(FACTORIAL['factorial'])
    print(compiler.build_function('factorial',
        ['a'], FACTORIAL['factorial']))
    assert False

def test_deep_call():
    """
    Test the output of::

        method factorial_test
            a : Z
        procedure
            b = factorial(a)
        end b
    """

    methods = backend.METHODS.copy()
    methods.update(FACTORIAL)

    compiler = backend.LLVMBackend(methods)
    compiler.build_function('factorial_test',
            ['a'], [
                Method('factorial_test',
                    {'a': INTEGERS},
                    {},
                    Node('factorial', {'a': Node('a', {})})
                    )
                ]
            )
    print(compiler.module)
    #compiler.module.verify()
    assert False
