"""
.. currentmodule:: fbml.analysis
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
##  class Modifier(object):
#    """
#    The modifier modifies a function.
#    """
#    def __init__(self, valueset):
#        self.valueset = valueset
#
#    def clean_function(self, function, args):
#        """
#        Cleans the methods using a valueset analysis, and
#        the signature of the methods.
#        """
#        if not self.evaluate_function(function, tuple(args)):
#            return FunctionNotValid(function, args)
#        valid_methods = []
#        for method in function.methods:
#            def clean_node(node, sources):
#                """ Sources is the clean nodes """
#                func, arglist = self.depends[node]
#                all_results = lambda m: [self.evaluate_method(m, args)
#                                         for args in arglist]
#                reached = [bool(
#                           reduce(
#                               self.valueset.merge,
#                               all_results(m),
#                               self.valueset.EXTREMUM
#                           ))
#                           for m in func.methods]
#
#                return fbml.node(model.SubFunction(func, reached), sources)
#
#            initial_map = {x: x for x in self.free_values(function)}
#            valid_methods.append(
#                model.Method(
#                    method.guard.visit(clean_node, initial_map),
#                    method.statment.visit(clean_node, initial_map)
#                ))
#
#        return function.define(function.constants, valid_methods)
#
#
#class FunctionNotValid(Exception):
#    """ Method is not valid """
