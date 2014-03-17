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
        return ("In Function {s.function!r} with {s.free_variables} free, " +
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

    def bind_variables(self, arguments, transform=lambda n, x: x):
        """
        Returns an dictionary with all the needed values bound,
        the tranform function, takes the input and transfroms it into
        a format know to the analysis.

        :param arguments:
            A dictionary filled with the arguments that the programer wants
            to bind to the function.

        :param transform:
            A function that transform any (allowed) object to an internal
            notion that can be used for further analysis. The function also
            takes a name of the variable to help context anaysis, As default it
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
            name: transform(name, value) for name, value in
            chain(arguments.items(), self.bound_value_pairs)
        }

    def __str__(self):
        return "{0.code}[{methods}]".format(
            self, methods=', '.join(str(method) for method in self.methods)
        )

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

    def __str__(self):
        if self.function.code == 'load':
            return str(self.named_sources[0].node)
        return "({0.function.code} {args})".format(
            self, args=" ".join("%s=%s" % s for s in self.named_sources)
        )

    @property
    def code(self):
        """ returns the code of the node """
        return 'n_' + hex(id(self))
