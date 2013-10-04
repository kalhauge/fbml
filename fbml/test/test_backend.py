"""
Tests the backend module

"""
from fbml.model import node, Method, link
from fbml.buildin import METHODS

from fbml import backend

def test_increment():
    """
    Single method::

        method increment
            a : Z
        procedure
            c = a + 1;
        end c

    """
    increment_node = node('add',(
        node('a'),
        node('c_1')
        ))

    interger_condition = node('Integer', (node('a'), ) )

    method = Method('increment', ['a'],
            {'c_1' : 1},
            interger_condition,
            increment_node)

    methods = METHODS + (method, )
    link(methods)
    back = backend.LLVMBackend()
    print(back.function_from_methods([method]))
    #assert False

def test_abs():
    """
    Two methods with conditions::

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
    node_b = node('neg', (node('a'), ) )
    abs_minus = Method('abs',
            ('a',),
            {'c': 0 },
            node('lt', (
                node('a'),
                node('c')
                )),
            node_b)

    node_b = node('a')
    abs_plus = Method('abs',
            ('a',),
            {'c': 0 },
            node('ge', (
                 node('a'),
                 node('c'))
                ),
            node_b)

    methods = METHODS + (abs_minus, abs_plus )
    link(methods)
    back = backend.LLVMBackend()
    print(back.function_from_methods([abs_minus, abs_plus]))
    # assert False

def test_clamp():
    """
    Tree methods with multible conditions::

        method clamp
            a <= high, a >= low
        procedure
        end a

        method clamp
            a > high
        procedure
        end high

        method clamp
            a < low
        procedure
        end low

    """
    high, low, node_a = node('high'), node('low'), node('a')

    clamp_middle = Method('clamp',
            ('a', 'low', 'high'),
            {},
            node('and',(
                node('le', (node_a, high) ),
                node('ge', (node_a, low) )
            )),
            node('a')
            )

    high, low, node_a = node('high'), node('low'), node('a')
    clamp_high = Method('clamp',
            ('a', 'low', 'high'),
            {},
            node('lt', (node_a, high)),
            node('high')
            )

    high, low, node_a = node('high'), node('low'), node('a')
    clamp_low = Method('clamp',
            ('a', 'low', 'high'),
            {},
            node('gt', (node_a, low) ),
            node('low'))

    methods = METHODS + (clamp_middle, clamp_high, clamp_low)
    link(methods)
    back = backend.LLVMBackend()
    func = back.function_from_methods(
        [clamp_middle, clamp_high, clamp_low])
    print(func)

INTERNAL_A = ( node('a'), node('a'), node('a'))
FACTORIAL = (
    Method('factorial',
        ('a', ),
        {'one': 1},
        node('and', {
            'a' : node('eq', {
                'a' : INTERNAL_A[0],
                'b' : node('one')
                }),
            'b' : node('Integer', {'value' : INTERNAL_A[0]}),
            }),
        node('a')
        ),
    Method('factorial',
        ('a', ),
        {'one': 1},
        node('and', {
            'a' : node('gt', {
                'a' : INTERNAL_A[1],
                'b' : node('one')
                }),
            'b' : node('Integer', {'value' : INTERNAL_A[1]}),
            }),
        node('mul',{
            'a' : node('factorial', {
                'a': node('sub', {
                    'a' : INTERNAL_A[2],
                    'b' : node('one')
                    }),
                }),
            'b' : INTERNAL_A[2]
            })
        ),
)

def test_factorial():
    """
    Test the output of::

        method factorial
            a == 1, a : Z
        procedure
        end a

        method factorial
            a > 1, a : Z
        procedure
            b = factorial(a - 1) * a
        end b

    """
    methods = METHODS + FACTORIAL
    link(methods)
    back = backend.LLVMBackend()
    func = back.function_from_methods(FACTORIAL)
    print(str(func))

def test_deep_call():
    """
    Test the output of::

        method factorial_test
            a : Z
        procedure
            b = factorial(a)
        end b
    """
    method = ( Method('factorial_test', ['a'],
                    {},
                    node('Integer',{'value': node('a')}),
                    node('factorial', {'a': node('a')})
                    ), )

    methods = METHODS + FACTORIAL + method
    link(methods)
    compiler = backend.LLVMBackend()
    compiler.function_from_methods(method)

    print(compiler.module)
    compiler.module.verify()

