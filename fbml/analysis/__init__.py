"""
.. currentmodule:: fbml.analysis
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
from collections import OrderedDict

from itertools import starmap, repeat
from functools import reduce

import logging
L = logging.getLogger(__name__)

from fbml import model


class Evaluator(object):

    """
    The evaluator can evaluate a function using some basic
    methods.

    :param eval_method:
        a function that evaluates a method.

    """

    def __init__(self, valueset):
        self.valueset = valueset
        self.dynamic = {}

    def evaluate_function(self, function, arguments):
        """ Evaluates a function """
        try:
            return self.dynamic[(function, arguments)]
        except KeyError:
            self.dynamic[(function, arguments)] = self.valueset.EXTREMUM
            while True:
                new = self._evaluate_function(function, arguments)
                if self.dynamic[(function, arguments)] == new:
                    break
                else:
                    self.dynamic[(function, arguments)] = new
            return new

    def _evaluate_function(self, function, arguments):
        valueset = self.valueset
        bound_values = OrderedDict({k : valueset.const(v)
                for k, v in function.constants.items()})
        bound_values.update(zip(function.arguments, arguments))
        method_calls = zip(function.methods, repeat(bound_values))
        values = starmap(self.evaluate_method, method_calls)
        return reduce(valueset.merge, values, valueset.EXTREMUM)


    def evaluate_method(self, method, initial):
        """ Evalutates a method """
        if isinstance(method, model.Method):
            test_value = self.evaluate_lattice(method.guard, initial)
            if self.valueset.allow(test_value):
                value = self.evaluate_lattice(method.statement, initial)
            else:
                value = self.valueset.EXTREMUM
            return value
        else:
            return self.valueset.apply(method, initial.values())

    def evaluate_lattice(self, node, initial):
        """ Evaluates a lattice """
        return node.visit(self.evaluate_node, initial)

    def evaluate_node(self, node, sources):
        """ Evaluates a single node """
        return self.evaluate_function(node.function, sources)

    def evaluate(self, function, args):
        """ Evaluates a function using real args """
        return self.evaluate_function(function,
                tuple(self.valueset.const(arg) for arg in args))

