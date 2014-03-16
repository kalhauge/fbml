"""
.. currentmodule:: fbml.visitor

Vistor consits of classes cabable of transversing the structure of the model,
bringing with it an value of any sort.

"""
from collections import namedtuple
from functools import reduce
from fbml import model


class Visitor(object):

    extremum = None

    @classmethod
    def run(cls, function, **arguments):
        return cls().call(function, **arguments)

    def call(self, function, **arguments):
        return self.visit_function(
            function, {
                name: self.transform(arg) for name, arg in arguments.items()
            })

    def allow(self, test):
        """
        Returns true or false depending on the test. In the default case we
        asume that this is a boolean return it.
        """
        return test

    def transform(self, value):
        """
        Given an value return a new value of the internal type, per default
        just returns the value itself.
        """
        return value

    def visit_function(self, function, arguments):
        """ visits a function

        :param function: The function to visit

        :param arguments: The arguments that the function should be called
            with. A dictionary containing the mapping from the values of the
            arguments to the function.
        """
        try:
            initial = function.bind_variables(arguments, self.transform)
        except model.BadBound:
            # For now do nothing
            raise
        else:
            results = [
                self.visit_buildin_method(method, initial) if method.is_buildin
                else self.visit_method(method, initial)
                for method in function.methods
            ]
            return self.exit_function(function, results)

    def visit_buildin_method(self, method, initial):
        return self.exit_buildin_method(
            method,
            tuple(initial[argname] for argname in method.argmap)
        )

    def visit_method(self, method, initial):
        """ visits a method

        :param method: The method to visit

        :param initial: The inital free variables, these variables should
            be a superset of the real need values
        """
        test_value = self.visit_nodes(method.guard, initial)
        if self.allow(test_value):
            nodes = self.visit_nodes(method.statement, initial)
            return self.exit_method(method, test_value, nodes)
        else:
            return self.extremum

    def visit_nodes(self, node, initial):
        """ visits a node tree """
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
        function = self.visit_function(node.function, node.project(sources))
        return self.exit_node(node, sources, function)

    def exit_function(self, function, results):
        raise NotImplementedError()

    def exit_buildin_method(self, method, args):
        raise NotImplementedError()

    def exit_method(self, method, guard, statement):
        raise NotImplementedError()

    def exit_node(self, node, sources, function):
        raise NotImplementedError()


class Evaluator(Visitor):

    def merge(self, first, second):
        """
        Merges two values as retured by methods. Should return a value of the
        internal type. The default version returns the first value that is not
        of the extremum.
        """
        return second if first == self.extremum else first

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

    Clean = namedtuple('Clean', ('result', 'tree'))

    def __init__(self, evaluator):
        self.evaluator = evaluator

    def visit_function(self, function, arguments):
        pass

    def merge(self, first, second):
        pass

    def apply(self, method, arguments):
        """ When applying somthing to a buildin_type means that is used"""
        return (self.evaluator.apply(method, arguments), arguments)
