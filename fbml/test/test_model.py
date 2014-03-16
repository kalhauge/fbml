"""
Tests of fbml.model
"""
from fbml.model import Function, Method, Node, BuildInMethod, BadBound
from fbml import node

from fbml.test import MUL_IF_LESS

from nose.tools import assert_equal, assert_raises, assert_regexp_matches

from unittest import TestCase
from unittest.mock import Mock


class FunctionTester(TestCase):

    def create_function(self):
        return Function({'x': None}, [
            Method(node('x'), node('y')),
            Method(node('y'), node('z'))
        ])

    def test_str(self):
        string = str(self.create_function())
        assert_regexp_matches(string, 'f0x[0-9abcdef]{8}')

    def test_repr(self):
        string = repr(Function({}, []))
        function = eval(string)
        assert_equal(function, Function({},[]))

    def test_repr_2(self):
        string = repr(self.create_function())
        function = eval(string)
        assert_equal(function, self.create_function())

    def test_free_vars(self):
        """
        Testing that the free_variables method works.
        This test should produce the free variables, z and y.
        """
        function = self.create_function()
        free_vars = function.free_variables()
        assert_equal(free_vars, {'z', 'y'})

    def test_mul_if_less_free_vars(self):
        """ Test if the free vars of MUL_IF_LESS is "number" """
        assert_equal(MUL_IF_LESS.free_variables(), {'number'})

    def test_bind_variables(self):
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

    def test_bind_variables_bad_bound(self):
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


class MethodTester (TestCase):

    def test_str(self):
        method = Method(node('a'), node('b'))
        string = str(method)
        assert_regexp_matches(string, 'a -> b')

    def test_repr(self):
        method = Method(node('a'), node('b'))
        string = repr(method)
        assert_equal(eval(string), method)

    def test_variables(self):
        """
        Testing that the variables of methods is returned correctly.
        """
        method = Method(node('x'), node('y'))
        variables = method.variables()
        assert_equal(variables, {'x', 'y'})

    def test_variables_with_internal_nodes(self):
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


class NodeTester (TestCase):

    def test_repr(self):
        n = node('a')
        string = repr(n)
        assert_equal(eval(string), n)

    def test_str(self):
        n = node('a')
        assert_equal(str(n), 'a')

    def test_str_lt(self):
        from fbml import buildin
        n = node(buildin.lt,  {'a': node('number'), 'b': node('const')})
        assert_equal(str(n), '(lt a=number b=const)')

    def test_str_function(self):
        f = Function({}, [], 'a_function')
        n = node(f,  {'a': node('number'), 'b': node('const')})
        assert_equal(str(n), '(a_function a=number b=const)')

    def test_depenencies(self):
        """
        Test that dependencies is returned correctly
        """
        n = node('x')
        assert_equal(n.dependencies(), {'x'})

    def test_depenencies_multible(self):
        """
        Test multible dependencies
        """
        n2 = Node(None, ((0, node('x')), (1, node('y'))))
        assert_equal(n2.dependencies(), {'x', 'y'})


class UtilsTester (TestCase):

    def test_node_creation(self):
        """ tests that nodes is created correctly """
        function = Mock(name="function")
        names = tuple("name" + str(i) for i in range(3))
        nodes = tuple("node" + str(i) for i in range(3))
        dictionary = dict(zip(names, nodes))
        assert_equal(
            Node(function, zip(names, nodes)),
            node(function, dictionary))

    def test_node_equality(self):
        """ Enusre that nodes created with same sources is equal """
        names = tuple("name" + str(i) for i in range(3))
        nodes = tuple("node" + str(i) for i in range(3))
        sources = list(zip(names, nodes))
        assert_equal(node(None, sources), node(None, reversed(sources)))


if __name__ == '__main__':
    import nose
    nose.runmodule(
        argv=[__file__, '-vvs', '-x', '--pdb'],
        exit=False
    )
