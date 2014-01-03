"""
.. currentmodule:: fbml.model
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>


:class:`Function`
=================

The function is a holder of bound_values, ei. constants, and a set of methods.


"""
from itertools import chain
from operator import itemgetter
from collections import namedtuple, deque

import logging
L = logging.getLogger(__name__)


class Function(namedtuple('Function', ['bound_values', 'methods'])):

    def free_variables(self):
        """
        Free variables is the variables that needs to be bound to the function
        for all of its methods to exceute. Calculated by finding the variables
        used in all of the methods, and removing the bound_values from the
        function.

        :param self:
            The function that we want to know the free variables of.

        :returns: The free variables of a function.
        """

        free_variables = set()
        for method in self.methods:
            free_variables.extend(method.variables)
        return free_variables - set(self.bound_values)

    def bind_variables(self, arguments):
        """
        Returns an dictionary with all the needed values bound
        """
        bound_vars = dict(chain(arguments, self.bound_values))
        # Assert might not be nesseary
        assert self.free_variables().issubset(bound_vars)
        return bound_vars

    def evaluate(self, analysis, arguments):
        """
        Returns an function able to evaluate the Function
        """
        initial = self.bind_variables(arguments)
        return reduce(
            analysis.merge,
            (method.evaluate(analysis, initial) for method in self.methods),
            analysis.EXTREMUM
        )


class Method(namedtuple('Method', ['guard', 'statement'])):

    def variables(self):
        """
        :param self:
            the method we want to find the variables from.

        :returns: the variables used by the method.
        """
        return set(
            node.function for node in chain(
                self.guard.precedes(),
                self.statement.precedes()
            ) if not node.sources
        )

    def evaluate(self, analysis, initial):
        assert self.variables().issubset(initial)
        test_value = self.guard.evaluate(analysis, initial)
        return self.statement.evaluate(analysis, initial)\
            if analysis.allow(test_value) else analysis.EXTREMUM


class BuildInMethod(namedtuple('BuildInMethod', ['argmap', 'code'])):

    def variables(self):
        """
        :param self:
            the method we want to find the variables from.

        :returns: the variables used by the method.
        """
        return set(self.argmap)

    def evaluate(self, analysis, initial):
        return analysis.apply(
            self,
            (initial[argname] for argname in self.argmap)
        )


class Node (namedtuple('Node', ['function', 'sources'])):
    """ Node """
    def precedes(self):
        """
        Returns the set of nodes that precedes the node. A node presedes an
        other node if there is an direct path from the second node to the first
        navigating thru the sources of the node.

        :param self:
            The node from wich to evaluate the dominating set of
            nodes

        :returns:
            all the nodes that precedes the node
        """
        visitors = deque((self,))
        nodes = set()

        while visitors:
            next_vistor = visitors.pop()
            nodes.add(next_vistor.sources)
            visitors.extendleft(next_vistor.sources)

        return nodes

    def precedes_in_order(self):
        """
        Like :func:`precedes`, but returns the preceding nodes in an partial
        orderd list
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

    def evaluate(self, analysis, initial):
        return self.visit(
            lambda node, sources: node.function.evaluate(analysis, sources),
            initial
        )

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
        return self.visit_all(visitor, initial)[self]

    def visit_all(self, visitor, initial):
        """ Returns the internal mapping for the visitor """
        mapping = dict(initial)
        for visit_node in reversed(self.nodes_in_order()):
            try:
                sources = tuple(mapping[s] for s in visit_node.sources)
                mapping[visit_node] = visitor(visit_node, sources)
            except KeyError:
                L.error("KeyError: %s, %s", visit_node, mapping)
                raise
        return mapping

    def __repr__(self):
        return 'Node(%s, %s)' % self

    @property
    def code(self):
        """ returns the code of the node """
        return hex(id(self))
