"""
.. currentmodule:: fbml.model
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
from functools import reduce
from operator import itemgetter
from collections import namedtuple, deque
from pprint import pformat

import logging
L = logging.getLogger(__name__)

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

    def evaluate(self, args, valueset):
        """
        predicts the return value using the valueset
        """
        allowed_values = self.allowed_subset(args, valueset)

        if self.is_buildin:
            return valueset.apply(self, allowed_values)
        else:
            initial = {i : valueset.const(v) for i, v in self.constants.items()}
            initial.update(zip(self.arguments, allowed_values))

            def evaluate_node(internal_node, sources):
                """
                evaluates a single node
                """
                if sources:
                    values = [m.evaluate(sources)
                            for m in internal_node.methods]
                    return reduce(valueset.union, values)
                else:
                    return initial[internal_node.name]

            return self.target.visit(evaluate_node)

    def allowed_subset(self, args, valueset):
        """
        Returns the allowed subset of the args.
        """
        return args

    @property
    def is_buildin(self):
        """
        checks if the method is buildin
        """
        return isinstance(self.target, str)

    def __repr__(self):
        return self.code

    @property
    def code (self):
        """
        Returns the code of the method
        """
        return self.name + "-" +  hex(id(self))

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

    def visit(self, function):
        """
        A visitor for nodes.

        :param basenode:
            The basenode is the lowest node in the graph

        :param function:
            Is the function that for each node returns anything
            . The function must accept a node, and a
            dictionary maping the old nodes to new values::

                function :=  Node x ?**k -> ?

        :returns:
            Whatever the function returns
        """
        mapping = {}
        for node in reversed(self.nodes_in_order()):
            sources = tuple(mapping[s] for s in node.sources)
            mapping[node] = function(node, sources)
        return mapping[self]

    def __repr__(self):
        return self.pformat()

    def pformat(self, indent=0):
        """
        returns a pretty fromatted str
        """
        newline = lambda ind: '\n' + '  '*ind

        def pformat_list(str_list, indent=0, paran = ('[', ']')):
            str_list = [s for s in str_list if s]
            if str_list:
                if len(str_list) == 1:
                    return paran[0] + str_list[0] + paran[1]
                else:
                    return (paran[0] +
                        newline(indent) +
                        (',' + newline(indent)).join(str_list) +
                        newline(indent) +
                        paran[1])
            else:
                return ''

        args = [
            repr(self.name),
            pformat_list(
                [s.pformat(indent+3) for s in self.sources],
                indent + 2),
            pformat_list(
                [m.code for m in self.methods],
                indent + 2)
            ]

        return 'node' + pformat_list(args, indent+1, ('(',')'))


    @property
    def code (self):
        return self.name + "-" +  hex(id(self))


def node(name, sources=tuple(), methods=tuple()):
    return Node(name, tuple(sources), tuple(methods))

