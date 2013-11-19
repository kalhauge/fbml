"""
.. currentmodule:: fbml.model
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
from itertools import chain, compress
from operator import itemgetter
from collections import namedtuple, deque

import logging
L = logging.getLogger(__name__)

from fbml.utils import frozendict

class Function(object):
    """
    The overall function
    """

    def __init__(self, name, arguments, constants, methods):
        self.name = name
        self.arguments = arguments
        self.constants = constants
        self.methods = methods

    def define(self, constants, methods):
        """ Defines the function """
        self.constants = constants
        self.methods = methods

    @classmethod
    def declare(cls, name, arguments):
        """ Declares a function """
        return cls(name, arguments, None, None)

    def __str__(self):
        return self.name

class SubFunction(object):
    """
    A function only pointing to a subset of the mehtods in
    the function
    """

    def __init__(self, function, method_filter):
        self.super_function = function
        self.method_filter = tuple(method_filter)

    @property
    def name(self):
        """ Proxy function for name """
        return self.super_function.name

    @property
    def arguments(self):
        """ Proxy function for arguments """
        return self.super_function.arguments

    @property
    def constants(self):
        """ Proxy function for constants """
        return self.super_function.constants

    @property
    def methods(self):
        """ Proxy function for methode """
        return compress(self.super_function.methods, self.method_filter)

class Method (namedtuple('Method', ['guard', 'statement'])):
    """ Method """

    is_buildin = False

class BuildInMethod(namedtuple('BuildInMethod', ['argmap', 'code'])):
    """ BuildInMethod """

    is_buildin = True

class Node (namedtuple('Node', ['function', 'sources'])):
    """ Node """

    def reachable_nodes(self):
        """
        Calculates reacable nodes
        """
        visitors = deque((self,))
        nodes = set()

        while visitors:
            next_vistor = visitors.pop()
            nodes.add(next_vistor.sources)
            visitors.extendleft(next_vistor.sources)

        return nodes

    def nodes_in_order(self):
        """
        Return the nodes in a partial ordering
        """
        node_numbers = {self : 0}

        visitors = deque((self,))
        while visitors:
            next_vistor = visitors.pop()
            if all(isinstance(s, Node) for s in next_vistor.sources):
                for source in next_vistor.sources:
                    node_numbers[source] = node_numbers[next_vistor] + 1
                visitors.extendleft(next_vistor.sources)

        return [node for node, index in
                    sorted(node_numbers.items(), key=itemgetter(1)) ]

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
        return self.visit_mapping(visitor, initial)[self]


    def visit_mapping(self, visitor, initial):
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
#
#    def pformat(self, indent=0):
#        """
#        returns a pretty fromatted str
#        """
#        newline = lambda ind: '\n' + '  '*ind
#
#        def pformat_list(str_list, indent, paran = ('[', ']')):
#            """ pretty formats a list """
#            str_list = [s for s in str_list if s]
#            if str_list:
#                if len(str_list) == 1:
#                    return_str = paran[0] + str_list[0] + paran[1]
#                else:
#                    return_str = (paran[0] +
#                        newline(indent) +
#                        (',' + newline(indent)).join(str_list) +
#                        newline(indent) +
#                        paran[1])
#            else:
#                return_str = ''
#            return return_str
#
#        args = [
#            pformat_list(
#                [str(self.function)] +
#                [s.pformat(indent + 3) for s in self.sources
#                    if isinstance(s, Node)],
#                indent + 2),
#            ]
#
#        return 'node' + pformat_list(args, indent+1, ('(',')'))


    @property
    def code (self):
        """ returns the code of the node """
        return hex(id(self))


