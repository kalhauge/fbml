"""
.. currentmodule:: fbml.model
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
from operator import itemgetter
import collections

import logging
L = logging.getLogger(__name__)

from fbml import value

class Method (object):
    """
     Method
     """

    def __init__(self, name, arguments, constants, target):
        self.name = name
        self.arguments = arguments
        self.constants = constants
        self.target = target

    def predict_value(self):
        return value.INTEGERS
#        values = {}
#        for node in reversed(self.target.nodes_in_order()):
#            if not node.sources:
#                try:
#                    value = method.constants[node.name]
#                except KeyError:
#                    value = method.arguments[node.name]
#            else:

    def __repr__(self):
        return self.name + '-' + str(id(self))


class Node (object):
    """
    Node
    """
    def __init__(self, name, sources):
        self.name = name
        self.sources = sources

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
