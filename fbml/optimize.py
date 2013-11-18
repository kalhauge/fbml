"""
.. currentmodule:: fbml.optimize
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
import itertools

import logging
L = logging.getLogger(__name__)

from fbml import model
from fbml.analysis import Evaluator


def clean_function(function, args, valueset):
    """
    Cleans the methods using a valueset analysis, and
    the signature of the methods.
    """



    initial = function.bound_values(valueset)
    for method in function.methods:
        initial = method.initial_values(args, valueset)
        def clean_node(node, sources):
            """ Sources is the clean nodes, and the arguments """
            if not sources:
                return initial[node.name], node
            else:
                args, nodes = zip(*sources)
                new_methods = [method for method in node.methods if
                        method.evaluate(args, valueset) != valueset.EXTREMUM]
                if not new_methods:
                    raise MethodNotValid(methods)
                new_node = model.node(SubFunction(), nodes)
                return_values = new_node.evaluate(args, valueset)
                return return_values, new_node

        method.constraint = method.constraint.visit(clean_node)[1]
        method.target     = method.target.visit(clean_node)[1]

    return methods





class MethodNotValid(Exception):
    """ Method is not valid """

