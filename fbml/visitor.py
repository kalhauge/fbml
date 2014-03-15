"""
.. currentmodule:: fbml.visitor

Vistor consits of classes cabable of transversing the structure of the model,
bringing with it an value of any sort.

"""

from fbml import model


class Visitor(object):

    extremum = None

    def transform(self, value):
        """
        Given an value return a new value of the internal type, per default
        just returns the value itself.
        """
        return value

    def merge(self, first, second):
        """
        Merges two values as retured by methods. Should return a value of the
        internal type. The default version returns the first value that is not
        of the extremum.
        """
        return second if first == self.extremum else first

    def allow(self, test):
        """
        Returns true or false depending on the test. In the default case we
        asume that this is a boolean return it.
        """
        return test

    def apply(self, method, arguments):
        """
        apply applies a method to the arguments, in the default case we hope
        that the method is callable and call it with the arguments.
        """
        return method(arguments)

    @classmethod
    def run(cls, function, **arguments):
        return cls().call(function, **arguments)

    def call(self, function, **arguments):
        return self.visit_function(
            function, {
                name: self.transform(arg) for name, arg in arguments.items()
            })

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
            work_value = self.extremum
            for method in function.methods:
                result = self.visit_method(method, initial)
                work_value = self.merge(work_value, result)
            return work_value

    def visit_method(self, method, initial):
        """ visits a method

        :param method: The method to visit

        :param initial: The inital free variables, these variables should
            be a superset of the real need values
        """
        if method.is_buildin:
            return self.apply(
                method, tuple(initial[argname] for argname in method.argmap)
            )
        else:
            test_value = self.visit_nodes(method.guard, initial)
            if self.allow(test_value):
                return self.visit_nodes(method.statement, initial)
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
        return self.visit_function(node.function, node.project(sources))
