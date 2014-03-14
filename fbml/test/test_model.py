"""
Tests of fbml.model
"""
from fbml.model import Function, Method, Node, BadBound
from fbml import node

from fbml.test import MUL_IF_LESS

from nose.tools import assert_equal, assert_raises

from unittest.mock import Mock


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


def test_mul_if_less_free_vars():
    """ Test if the free vars of MUL_IF_LESS is "number" """
    assert_equal(MUL_IF_LESS.free_variables(), {'number'})


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


def test_node_creation():
    """ tests that nodes is created correctly """
    function = Mock(name="function")
    names = tuple("name" + str(i) for i in range(3))
    nodes = tuple("node" + str(i) for i in range(3))
    dictionary = dict(zip(names, nodes))
    assert_equal(Node(function, zip(names, nodes)), node(function, dictionary))

def test_node_equality():
    """ Enusre that nodes created with same sources is equal """
    names = tuple("name" + str(i) for i in range(3))
    nodes = tuple("node" + str(i) for i in range(3))
    sources = list(zip(names, nodes))
    assert_equal(node(None, sources), node(None, reversed(sources)))

def test_variables():
    """
    Testing that the variables of methods is returned correctly.
    """
    method = Method(node('x'), node('y'))
    variables = method.variables()
    assert_equal(variables, {'x', 'y'})


def test_variables_with_internal_nodes():
    """
    Testing that variables is retured correctly, with internal nodes
    """
    from fbml import buildin
    method = Method(
        node(buildin.lt,  {'a': node('number'), 'b': node('const')}),
        node(buildin.mul, {'a': node('number'), 'b': node('const')})
    )
    variables = method.variables()
    assert_equal(variables, {'number', 'const'})


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
    n2 = Node(None, ((0, node('x')), (1, node('y'))))
    assert_equal(n2.dependencies(), {'x', 'y'})

if __name__ == '__main__':
    import nose
    nose.runmodule(
        argv=[__file__, '-vvs', '-x', '--pdb'],
        exit=False
    )
