"""

Tests of fbml.model

"""
from fbml.model import Function, Method, Node
from fbml import node

from nose.tools import assert_equal


def test_function_free_vars():
    """
    Testing that the free_variables method works.

    This test should produce the free variables, z and y.
    """
    function = Function({'x': None}, [
        Method(node('x'), node('y')),
        Method(node('y'), node('z'))
    ])

    free_vars = function.free_variables()
    assert_equal(free_vars, {'z', 'y'})


def test_variables():
    """
    Testing that the variables of methods is returned correctly.
    """
    method = Method(node('x'), node('y'))
    variables = method.variables()
    assert_equal(variables, {'x', 'y'})


def test_depenencies():
    """
    Test that dependencies is returned correctly
    """
    n = node('x')
    assert_equal(n.dependencies(), {'x'})


def test_depenencies_multible():
    """
    Test multible dependencies
    """
    n2 = Node(None, (node('x'), node('y')), None)
    assert_equal(n2.dependencies(), {'x', 'y'})

