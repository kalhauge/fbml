"""
.. currentmodule:: fbml.model
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
from operator import itemgetter
from collections import namedtuple, deque

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


class Node (namedtuple('Node', ['name', 'sources', 'methods'])):
    """
    Node
    """
    def calulate_reach(self):
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
            for source in next_vistor.sources:
                node_numbers[source] = node_numbers[next_vistor] + 1
            visitors.extendleft(next_vistor.sources)

        return [node for node, index in
                    sorted(node_numbers.items(), key=itemgetter(1)) ]

    def __repr__(self):
        return self.name + "-" +  str(id(self))

def node(name, sources=tuple(), methods=tuple()):
    return Node(name, tuple(sources), tuple(methods))

def visit(basenode, function):
    """
    A visitor for nodes.

    :param basenode:
        The basenode is the lowest node in the graph

    :param function:
        Is the function that for each node returns anything
        . The function must accept a node, and a
        dictionary maping the old nodes to new values::

            function :=  Node, ( Node -> ? ) -> ?

    :returns:
        Whatever the function returns
    """
    mapping = {}
    for node in reversed(basenode.nodes_in_order()):
        mapping[node] = function(node, mapping)
    return mapping[basenode]

def link(methods):
    """
    Links the nodes to the methods
    """
    named_methods = {}
    for method in methods:
        named_methods.setdefault(method.name, []).append(method)

    def add_methods(old_node, sources):
        """
        Add methods to nodes, and returs a new node
        """
        if old_node.sources:
            return node(old_node.name,
                    tuple(sources[src] for src in old_node.sources),
                    named_methods[old_node.name])
        else:
            return old_node

    for method in methods:
        method.contraint = visit(method.contraint, add_methods)
        if not method.is_buildin():
            method.target = visit(method.target, add_methods)

