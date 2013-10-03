"""
Tests the backend module

"""
import llvm.core as llvmc

from nose.tools import nottest, assert_equals

from fbml.model import Node, Method, link
from fbml.value import INTEGERS, singleton
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
    increment_node = Node('add', {
        'a': Node('a'),
        'b': Node('c_1')
        })

    interger_condition = Node('Integer', {
                'number': Node('a')
                })

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
    node_b = Node('neg', {'a': Node('a') })
    abs_minus = Method('abs',
            ('a',),
            {'c': 0 },
            Node('lt', {
                'a': Node('a'),
                'b': Node('c')}
                ),
            node_b)

    node_b = Node('a')
    abs_plus = Method('abs',
            ('a',),
            {'c': 0 },
            Node('ge', {
                'a': Node('a'),
                'b': Node('c')}
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
    high, low, node_a = Node('high'), Node('low'), Node('a')

    clamp_middle = Method('clamp',
            ('a', 'low', 'high'),
            {},
            Node('and', {
                'a': Node('le', { 'a': node_a, 'b': high }),
                'b': Node('ge', { 'a': node_a, 'b': low })
            }),
            Node('a')
            )

    high, low, node_a = Node('high'), Node('low'), Node('a')
    clamp_high = Method('clamp',
            ('a', 'low', 'high'),
            {},
            Node('lt', { 'a': node_a, 'b': high }),
            Node('high')
            )

    high, low, node_a = Node('high'), Node('low'), Node('a')
    clamp_low = Method('clamp',
            ('a', 'low', 'high'),
            {},
            Node('gt', { 'a': node_a, 'b': low }),
            Node('low'))

    methods = METHODS + (clamp_middle, clamp_high, clamp_low)
    link(methods)
    back = backend.LLVMBackend()
    func = back.function_from_methods(
        [clamp_middle, clamp_high, clamp_low])
    print(func)

INTERNAL_A = ( Node('a'), Node('a'), Node('a'))
FACTORIAL = (
    Method('factorial',
        ('a', ),
        {'one': 1},
        Node('and', {
            'a' : Node('eq', {
                'a' : INTERNAL_A[0],
                'b' : Node('one')
                }),
            'b' : Node('Integer', {'value' : INTERNAL_A[0]}),
            }),
        Node('a')
        ),
    Method('factorial',
        ('a', ),
        {'one': 1},
        Node('and', {
            'a' : Node('gt', {
                'a' : INTERNAL_A[1],
                'b' : Node('one')
                }),
            'b' : Node('Integer', {'value' : INTERNAL_A[1]}),
            }),
        Node('mul',{
            'a' : Node('factorial', {
                'a': Node('sub', {
                    'a' : INTERNAL_A[2],
                    'b' : Node('one')
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
                    Node('Integer',{'value': Node('a')}),
                    Node('factorial', {'a': Node('a')})
                    ), )

    methods = METHODS + FACTORIAL + method
    link(methods)
    compiler = backend.LLVMBackend()
    compiler.function_from_methods(method)

    print(compiler.module)
    compiler.module.verify()

