"""

Tests of fbml.model

"""
from fbml.model import Function, Method, Node, BadBound
from fbml import node

from nose.tools import assert_equal, assert_raises


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


def test_bind_variables():
    """
    Test binding of values
    """
    function = Function({'x': 4}, [
        Method(node('x'), node('y')),
        Method(node('y'), node('z'))
    ])

    bound = function.bind_variables({'y': 10, 'z': 20})
    assert_equal(bound, {'x': 4, 'y': 10, 'z': 20})

    bound = function.bind_variables({'y': 10, 'z': 20}, str)
    assert_equal(bound, {'x': '4', 'y': '10', 'z': '20'})


def test_bind_variables_bad_bound():
    """
    Test that the bind_variables throw the bad_bound exception
    """
    function = Function({'x': None}, [
        Method(node('x'), node('y')),
        Method(node('y'), node('z'))
    ])
    with assert_raises(BadBound):
        function.bind_variables({})

    with assert_raises(BadBound):
        function.bind_variables({'x': 12, 'y': 10, 'z': 4})

    with assert_raises(BadBound):
        function.bind_variables({'y': 10})


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
