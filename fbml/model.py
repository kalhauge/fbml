"""
.. currentmodule:: fbml.model
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
from functools import reduce
from operator import itemgetter
from collections import namedtuple, deque
from collections.abc import abstractmethod

import logging
L = logging.getLogger(__name__)

class AbstactMethod (object):
    """
    An AbstractMethod
    """

    code = 'abstract'

    @abstractmethod
    def evaluate(self, args, valueset):
        """ Evaluates the method using the args """

    @abstractmethod
    def initial_values(self, args, valueset):
        """ Returst the dict pointing to the initial_values """

    def __repr__(self):
        return self.code

class Method (AbstactMethod):
    """
     Method
     """

    is_buildin = False

    def __init__(self, name, arguments, constants, contraint, target):
        # pylint: disable = R0913
        self.name = name
        self.arguments = arguments
        self.constants = constants
        self.contraint = contraint
        self.target = target

    def evaluate(self, args, valueset):
        """
        predicts the return value using the valueset
        """
        L.debug("evaluating %s%s", self, args)

        if self.allow(args, valueset):
            initial = self.initial_values(args, valueset)
            L.debug("%s inital values: %s", self, initial)
            value =  self.target.evaluate(initial, valueset)
            L.debug('%s returns : %s', self, value)
            return value
        else:
            return valueset.min

    def allow(self, argset, valueset):
        """
        Returns if the args is a  allowed subset.

        This is not working apporpriate

        """
        initial = self.initial_values(argset, valueset)
        result = self.contraint.evaluate(initial, valueset)
        truth = True in result and not False in result
        L.debug('%s is allowed' if truth else '%s is not allowed', self)
        return truth

    def initial_values(self, argset, valueset):
        """
        :returns: the intial values of a execution using
        the argset
        """
        initial = {i : valueset.const(v) for i, v in self.constants.items()}
        initial.update(zip(self.arguments, argset))
        return initial

    @property
    def code (self):
        """
        Returns the code of the method
        """
        return self.name + "-" +  hex(id(self))

class BuildInMethod(AbstactMethod):

    """
    BuildInMethod

    """

    is_buildin = True

    def __init__(self, name, arguments, code):
        self.name = name
        self.arguments = arguments
        self.code = code

    def evaluate(self, argsset, valueset):
        return valueset.apply(self, argsset)

    def initial_values(self, argset, valueset):
        return dict(zip(self.arguments, argset))

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
        for visit_node in reversed(self.nodes_in_order()):
            sources = tuple(mapping[s] for s in visit_node.sources)
            mapping[visit_node] = function(visit_node, sources)
        return mapping[self]

    def evaluate(self, initial, valueset):
        """ Evaluate helper function """

        L.debug('%s %s', self.code, self.methods)

        def evaluate_node(internal_node, sources):
            """ evaluates a single node """
            if sources:
                values = [m.evaluate(sources, valueset)
                        for m in internal_node.methods]
                return reduce(valueset.union, values, valueset.min)
            else:
                return initial[internal_node.name]

        return self.visit(evaluate_node)

    def __repr__(self):
        return self.pformat()

    def pformat(self, indent=0):
        """
        returns a pretty fromatted str
        """
        newline = lambda ind: '\n' + '  '*ind

        def pformat_list(str_list, indent, paran = ('[', ']')):
            """ pretty formats a list """
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
        """ returns the code of the node """
        return self.name + "-" +  hex(id(self))


def node(name, sources=tuple(), methods=tuple()):
    """ Simple constructor for a node """
    return Node(name, tuple(sources), tuple(methods))

