"""
.. currentmodule:: fbml.analysis
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
from collections import OrderedDict

from itertools import starmap, repeat, chain
from functools import reduce

import logging
L = logging.getLogger(__name__)

from fbml import model
import fbml


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
        self.depends = {}

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

    def bound_values(self, function, arguments):
        """ Bound values of a  function """
        bound_values = OrderedDict({k : self.valueset.const(v)
                for k, v in function.constants.items()})
        bound_values.update(zip(function.arguments, arguments))
        return bound_values

    def free_values(self, function):
        """ Returns the free values of the methods """
        return chain(function.arguments, function.constants)

    def _evaluate_function(self, function, arguments):
        """ internal function for evaluating a function """
        valueset = self.valueset
        bound_values = self.bound_values(function, arguments)
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
        self.depends[node] = node.function, sources
        return self.evaluate_function(node.function, sources)

    def evaluate(self, function, args):
        """ Evaluates a function using real args """
        return self.evaluate_function(function,
                tuple(self.valueset.const(arg) for arg in args))


class Modifier(object):

    def __init__(self, valueset):
        self.valueset = valueset

    def clean_function(self, function, args):
        """
        Cleans the methods using a valueset analysis, and
        the signature of the methods.
        """
        if not self.evaluate_function(function, tuple(args)):
            return FunctionNotValid(function, args)
        valid_methods = []
        for method in function.methods:
            def clean_node(node, sources):
                """ Sources is the clean nodes """
                func, arglist = self.depends[node]
                all_results = lambda m : [self.evaluate_method(m, args)
                         for args in arglist]
                reached = [bool(
                            reduce(
                                self.valueset.merge,
                                all_results(m),
                                self.valueset.EXTREMUM
                            ))
                            for m in func.methods]

                return fbml.node(model.SubFunction(func, reached), sources)


            initial_map = {x:x for x in self.free_values(function) }
            valid_methods.append(
                    model.Method(
                        method.guard.visit(clean_node, initial_map ),
                        method.statment.visit(clean_node, initial_map)
                        ))

        return function.define(function.constants, valid_methods)


class FunctionNotValid(Exception):
    """ Method is not valid """

