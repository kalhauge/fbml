"""
.. currentmodule:: fbml.model
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
from operator import itemgetter
from collections import namedtuple, deque
from pprint import pformat

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
        """ Aproximating the allowed values
        """
        return { a : INTEGERS for a in self.arguments }

    def is_buildin(self):
        """
        checks if the method is buildin
        """
        return isinstance(self.target, str)

    def __repr__(self):
        return self.code

    @property
    def code (self):
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

