"""
.. currentmodule:: fbml.visitor

Vistor consits of classes cabable of transversing the structure of the model,
bringing with it an value of any sort.

"""
from collections import namedtuple
from functools import reduce

import logging
L = logging.getLogger(__name__)

from fbml import model


class Visitor(object):

    extremum = None

    @classmethod
    def run(cls, function, **arguments):
        return cls().call(function, **arguments)

    def call(self, function, **arguments):
        return self.visit_function(
            function, {
                name: self.transform(name, arg)
                for name, arg in arguments.items()
            })

    def visit_function(self, function, arguments):
        """ visits a function

        :param function: The function to visit

        :param arguments: The arguments that the function should be called
            with. A dictionary containing the mapping from the values of the
            arguments to the function.
        """
        L.debug(">visit_function       %s %s", function, arguments)
        try:
            initial = function.bind_variables(arguments, self.transform)
        except model.BadBound as e:
            L.error("<visit_function       %s %s", function, e)
            raise
        else:
            results = [
                self.visit_buildin_method(method, initial) if method.is_buildin
                else self.visit_method(method, initial)
                for method in function.methods
            ]

            result = self.exit_function(function, results)
            L.debug("<visit_function       %s %s", function, result)
            return result

    def visit_buildin_method(self, method, initial):
        L.debug(">visit_buildin_method %s %s", method, initial)
        result = self.exit_buildin_method(
            method,
            tuple(initial[argname] for argname in method.argmap)
        )
        L.debug("<visit_buildin_method %s %s", method, result)
        return result

    def visit_method(self, method, initial):
        """ visits a method

        :param method: The method to visit

        :param initial: The inital free variables, these variables should
            be a superset of the real need values
        """
        L.debug(">visit_method         %s %s", method, initial)
        test_value = self.visit_nodes(method.guard, initial)
        if self.allow(test_value):
            nodes = self.visit_nodes(method.statement, initial)
            result = self.exit_method(method, test_value, nodes)
        else:
            result = self.extremum
        L.debug("<visit_method         %s %s", method, result)
        return result

    def visit_nodes(self, node, initial):
        """ visits a node tree """
        #L.debug("visit_nodes %s %s", node, initial)
        mapping = dict(initial)
        for visit_node in reversed(node.precedes()):
            sources = tuple(mapping[s] for s in visit_node.sources)
            mapping[visit_node] = self.visit_node(visit_node, sources)
        return mapping[node]

    def visit_node(self, node, sources):
        """ visits a node

        :param node: The head node

        :param sources: The sources in order
        """
        L.debug(">visit_node           %s %s", node, sources)
        function = self.visit_function(node.function, node.project(sources))
        result = self.exit_node(node, sources, function)
        L.debug("<visit_node           %s %s", node, result)
        return result

    def allow(self, test):
        """
        Returns true or false depending on the test.
        """
        raise NotImplementedError()

    def transform(self, name, value):
        """
        Given an value return a new value of the internal type.
        """
        raise NotImplementedError()

    def exit_function(self, function, results):
        raise NotImplementedError()

    def exit_buildin_method(self, method, args):
        raise NotImplementedError()

    def exit_method(self, method, guard, statement):
        raise NotImplementedError()

    def exit_node(self, node, sources, function):
        raise NotImplementedError()


class Evaluator(Visitor):

    def failed(self, result):
        return result is self.extremum

    def merge(self, first, second):
        """
        Merges two values as retured by methods. Should return a value of the
        internal type. The default version returns the first value that is not
        of the extremum.
        """
        return second if self.failed(first) else first

    def merge_all(self, values):
        """
        Merges multible values at once, overload to get better controll over
        the situation.
        """
        return reduce(self.merge, values, self.extremum)

    def apply(self, method, arguments):
        """
        apply applies a method to the arguments, in the default case we hope
        that the method is callable and call it with the arguments.
        """
        return method(arguments)

    def exit_function(self, function, results):
        return self.merge_all(results)

    def exit_buildin_method(self, method, args):
        return self.apply(method, args)

    def exit_method(self, method, guard, statement):
        return statement if self.allow(guard) else self.extremum

    def exit_node(self, node, sources, function):
        return function


class Cleaner(Visitor):

    """
    A Cleaner is a special vistior that using an evalutor can create clean
    methods and functions by removeing anything that is no reacable by the
    evaluator. This means using an evaluator with an overapproxtion would
    be the best way to go.

    :param evaluator: The instanciated evaluator
    """

    Clean = namedtuple('Clean', ('model', 'result'))
    Clean.__str__ = lambda self: \
        "Clean(model={0.model}, result={0.result})".format(self)

    def __init__(self, evaluator):
        self.evaluator = evaluator
        self.extremum = self.Clean(None, self.evaluator.extremum)

    def call(self, function, **arguments):
        return super(Cleaner, self).call(function, **arguments).model

    def unzip(self, values):
        return (
            [value.model for value in values],
            [value.result for value in values]
        )

    def transform(self, name, value):
        if isinstance(value, self.Clean):
            return value
        else:
            return self.Clean(name, self.evaluator.transform(name, value))

    def allow(self, test):
        L.debug('Cleaner.allow %s', test)
        result = self.evaluator.allow(test.result) and test.model
        L.debug('Cleaner.allow %s', (result, ))
        return result

    def exit_function(self, function, results):
        models, results_ = self.unzip(results)
        methods = [
            method for method, result in results
            if not self.evaluator.failed(result)
        ]
        return self.Clean(
            model.Function(function.bound_values, methods, function.name),
            self.evaluator.exit_function(function, results_)
        )

    def exit_buildin_method(self, method, args):
        models, results = self.unzip(args)
        result = self.evaluator.exit_buildin_method(method, results)
        return self.Clean(method, result)

    def exit_method(self, method, guard, statement):
        L.debug('exit_method %s %s %s', method, guard, statement)
        return self.Clean(
            model.Method(guard.model, statement.model),
            self.evaluator.exit_method(method, guard.result, statement.result)
        )

    def exit_node(self, node, sources, function):
        models, results = self.unzip(sources)
        return self.Clean(
            model.Node(function.model, zip(node.names, models)),
            self.evaluator.exit_node(node, results, function.result)
        )
