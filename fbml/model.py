"""
.. currentmodule:: fbml.model
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
from operator import itemgetter
import collections

import logging
L = logging.getLogger(__name__)

from fbml.value import INTEGERS, union

class Method (object):
    """
     Method
     """

    def __init__(self, name, arguments, constants, contraint, target):
        self.name = name
        self.arguments = arguments
        self.constants = constants
        self.contraint = contraint
        self.target = target

    def predict_return(self, compare=union):
        """
        predicts the return value
        """
        return INTEGERS

    def allowed_arguments(self, compare=union):
        """
        Aproximating the allowed values
        """
        return { a : INTEGERS for a in self.arguments }

    def is_buildin(self):
        """
        checks if the method is buildin
        """
        return isinstance(self.target, str)

    def __repr__(self):
        return self.name + '-' + hex(id(self))


class Node (object):
    """
    Node
    """
    def __init__(self, name, sources=None, methods=None):
        self.name = name
        if not sources:
            sources = {}
        self.sources = sources.copy()
        if not methods:
            methods = tuple()
        self.methods = tuple(methods)

    def calulate_reach(self):
        """
        Calculates reacable nodes
        """
        visitors = collections.deque((self),)
        nodes = set()

        while visitors:
            next_vistor = visitors.pop()
            nodes.add(next_vistor.sources.values())
            visitors.extendleft(next_vistor.sources.values())

        return nodes

    def nodes_in_order(self):
        """
        Return the nodes in a partial ordering
        """
        node_numbers = {self : 0}

        visitors = collections.deque((self,))
        while visitors:
            next_vistor = visitors.pop()
            for source in next_vistor.sources.values():
                node_numbers[source] = node_numbers[next_vistor] + 1
            visitors.extendleft(next_vistor.sources.values())

        return [node for node, index in
                    sorted(node_numbers.items(), key=itemgetter(1)) ]

    def __repr__(self):
        return self.name + "-" +  str(id(self))


def link(methods):
    """
    Links the nodes to the methods
    """
    named_methods = {}
    for method in methods:
        named_methods.setdefault(method.name, []).append(method)

    for method in methods:
        add_methods(method.contraint, named_methods)
        if not method.is_buildin():
            add_methods(method.target, named_methods)


def add_methods(basenode, named_methods):
    """
    add methods to a porgram graph
    """
    nodes = reversed(basenode.nodes_in_order())
    for node in nodes:
        if node.sources:
            node.methods = named_methods[node.name]



