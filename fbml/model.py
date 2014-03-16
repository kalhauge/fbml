"""

.. currentmodule:: fbml.model
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>
.. verion:: 1.0

:class:`Function`
=================

The function is a holder of bound_values, ei. constants, and a set of methods.


"""
from itertools import chain
from operator import itemgetter
from collections import namedtuple, deque
from functools import reduce

import logging
L = logging.getLogger(__name__)


class BadBound(Exception):
    """ Bad bound error, cast if there is an inconsistence between
        free_variables and arguments.
    """
    def __init__(self, function, free_variables, arguments):
        super(BadBound, self).__init__()
        self.function = function
        self.free_variables = free_variables
        self.arguments = arguments

    def __str__(self):
        return ("In Function {s.function} with {s.free_variables} free, " +
                "received arguments {s.arguments}").format(s=self)


class Function(namedtuple('Function', [
        'bound_value_pairs', 'methods', 'name'])):
    """
    The top object of the bunch.
    """
    BoundValue = namedtuple('BoundValue', ['name', 'value'])
    BoundValue.__repr__ = lambda self: \
        'Function.BoundValue(name={0.name!r}, value={0.value!r})'.format(self)

    def __new__(cls, bound_value_pairs, methods, name=None):
        # Assumes dictionary to simplify interface
        bound_values = dict(bound_value_pairs).items()
        items = tuple(sorted(bound_values, key=itemgetter(0)))
        s = super(Function, cls).__new__(cls, items, tuple(methods), name)
        s._hash = hash(s)
        return s

    def hash(self):
        return self._hash

    @property
    def bound_values(self):
        return dict(self.bound_value_pairs)

    def free_variables(self):
        """
        Free variables is the variables that needs to be bound to the function
        for all of its methods to exceute. Calculated by finding the variables
        used in all of the methods, and removing the bound_values from the
        function.

        :param self:
            The function that we want to know the free variables of.

        :returns: The set of free variables of a function.
        """

        free_vars = [method.variables() for method in self.methods]
        return (set.union(*free_vars) -
                set(name for name, value in self.bound_value_pairs))

    def bind_variables(self, arguments, transform=lambda x: x):
        """
        Returns an dictionary with all the needed values bound,
        the tranform function, takes the input and transfroms it into
        a format know to the analysis.

        :param arguments:
            A dictionary filled with the arguments that the programer wants
            to bind to the function.

        :param transform:
            A function that transform any (allowed) object to an internal
            notion that can be used for further analysis. As default it
            does nothing, and allow all values.

        :raises BadBound:
            Exception if that arguments is not filling the entire free_variable
            space, or if in overlapping with the allready bound variables.
            For more infomation see :class:`BadBound`.

        :returns:
            A dictionary with all the bound values, a union of the already
            bound values of the function, and the presented arguments. All
            values presented in a format allowed by the transform
        """
        free_variables = self.free_variables()
        if free_variables != set(arguments):
            raise BadBound(self, free_variables, arguments)
        return {
            name: transform(value) for name, value in
            chain(arguments.items(), self.bound_value_pairs)
        }

    def evaluate(self, analysis, arguments):
        """
        Evaluates the function, by runing the methods using the arguments,
        the analysis is provided to describe how this is handled.
        """
        initial = self.bind_variables(arguments, analysis.transform)
        return reduce(
            analysis.merge,
            (method.evaluate(analysis, initial) for method in self.methods),
            analysis.EXTREMUM
        )

    def clean(self, analysis, arguments):
        """
        Cleans a function by returning a function, that do not contain
        unrachable methods, if executed from the arguments.  The cleaning is
        done recursively.
        """
        initial = self.bind_variables(arguments, analysis.transform)
        cleaned_methods = [
            method.clean(analysis, initial) for method in self.methods
        ]
        good_methods = [method for method in cleaned_methods if method]
        L.debug('CLEAN: %s(%s) -> %s -> %s',
                self.code,
                ', '.join('%s=%s' % x for x in initial.items()),
                cleaned_methods, good_methods)
        return Function(self.bound_values, good_methods, self.name)

    def __str__(self):
        return self.code

    @property
    def code(self):
        if self.name:
            return self.name
        else:
            return 'f' + hex(id(self))


class Method(namedtuple('Method', ['guard', 'statement'])):
    """
    The method is the branching part of the model, each method contains of a
    guard and a statement, a method will not execute unless a guard evaluates
    to true.

    """

    is_buildin = False

    def variables(self):
        """
        A method which finds the variables used by the method to execute,
        before all variables is ready a method, cannot fire.

        :returns: the variables used by the method.
        """
        return set(
            node for node in chain(
                self.guard.dependencies(),
                self.statement.dependencies()
            ) if not isinstance(node, Node)
        )

    def evaluate(self, analysis, initial):
        assert self.variables().issubset(initial)
        test_value = self.guard.evaluate_all(analysis, initial)
        return self.statement.evaluate_all(analysis, initial)\
            if analysis.allow(test_value) else analysis.EXTREMUM

    def clean(self, analysis, initial):
        test, guard = self.guard.clean(analysis, initial)
        result, statement = self.statement.clean(analysis, initial)
        return Method(guard, statement)\
            if analysis.allow(test) and statement else None

    def __str__(self):
        return "{0.guard!s} -> {0.statement!s}".format(self)


class BuildInMethod(namedtuple('BuildInMethod', ['argmap', 'code'])):
    """
    The build in methods is special methods that does not contain a subflow.
    These entities is therefor build in and unchangeable.

    A build in method has two attributes a :attr:`argmap` and a :attr:`code`
    attribute. The argmap is the argumentnames in the oder in which that they
    should be called oppon the lower hardwar leves. The code attribute is the
    buildin name, which can be used when building backends.
    """

    is_buildin = True

    def variables(self):
        """
        Same as in the Method, but in the build in method this is all
        found in advance.

        :returns: the variables used by the method.
        """
        return set(self.argmap)

    def evaluate(self, analysis, initial):
        return analysis.apply(
            self,
            tuple(initial[argname] for argname in self.argmap)
        )

    def clean(self, analysis, initial):
        result = analysis.apply(
            self,
            tuple(initial[argname] for argname in self.argmap))
        return self if result else None

    def __str__(self):
        return self.code


class Node (namedtuple('Node', ['function', 'named_sources'])):
    """
    Node, if the function is load, then the sources are allowed to be a string
    """

    Source = namedtuple('Source', ['name', 'node'])
    Source.__repr__ = lambda self: \
        'Node.Source(name={0.name!r}, node={0.node!r})'.format(self)

    def __new__(cls, function, named_sources):
        """
        New sorts the sources and puts them in the Source folder for later ease
        of test of equality
        """
        named_sources = (cls.Source(name, node)
                         for name, node in named_sources)
        sorted_sources = tuple(
            sorted(named_sources, key=lambda source: source.name)
        )
        return super(Node, cls).__new__(cls, function, sorted_sources)

    def dependencies(self):
        """
        Returns the dependencies of executing the node, ei the names of the
        variables that should exist in initial values
        """
        sources = chain.from_iterable(node.sources for node in self.precedes())
        return {
            source for source in sources if not isinstance(source, Node)
        }

    @property
    def names(self):
        return (source.name for source in self.named_sources)

    @property
    def sources(self):
        return (source.node for source in self.named_sources)

    def precedes(self):
        """
        Returns the set of nodes that precedes the node. A node precedes an
        other node if there is an direct path from the second node to the first
        navigating thru the sources of the node.

        The nodes are returned in order.

        :param self:
            The node from wich to evaluate the dominating set of
            nodes

        :returns:
            all the nodes that precedes the node
        """
        node_numbers = {self: 0}

        visitors = deque((self,))
        while visitors:
            next_vistor = visitors.pop()
            if all(isinstance(s, Node) for s in next_vistor.sources):
                for source in next_vistor.sources:
                    node_numbers[source] = node_numbers[next_vistor] + 1
                visitors.extendleft(next_vistor.sources)

        return [node for node, index in
                sorted(node_numbers.items(), key=itemgetter(1))]

    def project(self, values):
        """
        Projects the values onto the names of the function

        :returns:
            A dict containing the value, name pairs.
        """
        return dict(zip(self.names, values))

    def visit(self, visitor, initial):
        """
        A visitor for nodes.

        :param visitor:
            Is the function that for each node returns anything.  The visitor
            must accept a node, and a dictionary maping the old nodes to new
            values::

                visitor :=  Node x ?**k -> ?

        :returns:
            Whatever the visitor returns
        """
        return self._visit(visitor, initial)[self]

    def _visit(self, visitor, initial):
        """ Returns the internal mapping for the visitor """
        mapping = dict(initial)
        for visit_node in reversed(self.precedes()):
            try:
                sources = tuple(mapping[s] for s in visit_node.sources)
                mapping[visit_node] = visitor(visit_node, sources)
            except KeyError as e:
                L.error("When visiting (%r) recieved %r in %s", visit_node, e, mapping)
                raise
        return mapping

    def evaluate(self, analysis, sources):
        return self.function.evaluate(analysis, sources)

    def evaluate_all(self, analysis, initial):
        return self.visit(
            lambda node, sources: node.evaluate(
                analysis, node.project(sources)
            ),
            initial
        )

    def clean(self, analysis, initial):
        mapping = {
            name: (val, name) for name, val in initial.items()
        }

        def cleanup(node, sources):
            results, nodes = zip(*sources)
            projected = node.project(results)
            new_function = node.function.clean(analysis, projected)
            values = {source: projected[name] for name, source in node.named_sources}
            result = node.evaluate_all(analysis, values)
            return (result, Node(new_function, zip(node.names, nodes)))

        return self.visit(cleanup, mapping)

    def __str__(self):
        if self.function.code == 'load':
            return self.named_sources[0].node
        return "({0.function.code} {args})".format(
            self, args=" ".join("%s=%s" % s for s in self.named_sources)
        )

    @property
    def code(self):
        """ returns the code of the node """
        return 'n_' + hex(id(self))


class ReduceNode(namedtuple('ReduceNode', [
    'function',
    'reduction',
    'names',
    'sources'
])):

    dependencies = Node.dependencies
    precedes = Node.precedes
    visit = Node.visit
    _visit = Node._visit
    clean = Node.clean

    def evaluate(self, analysis, sources):
        return analysis.reduce(self.function, self.reduction, sources)

    evaluate_all = Node.evaluate_all

    def __str__(self):
        return 'ReduceNode %s:\n    %s,\n    %s\n)' % (
            self.function.code + str(self.function.methods),
            ('(\n    ' + ',\n    '.join(
                repr(source) for source in self.sources
            ) + '\n)').replace('\n', '\n    '),
            self.names)

    def __repr__(self):
        return 'ReduceNode %s: %r' % (self[0].code, self.sources)
