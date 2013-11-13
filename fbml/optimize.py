"""
.. currentmodule:: fbml.optimize
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
import itertools

import logging
L = logging.getLogger(__name__)

from fbml import model
from fbml.analysis import typeset

def link(methods):
    """
    Links the nodes to the methods
    """
    named_methods = {}
    # Created the method table
    for method in methods:
        named_methods.setdefault(method.name, []).append(method)

    def add_methods(old_node, sources):
        """
        Add methods to nodes, and returs a new node
        """
        if sources:
            return model.node(old_node.name,
                    sources, named_methods[old_node.name])
        else:
            return old_node

    for method in (m for m in methods if not m.is_buildin):
        method.constraint = method.constraint.visit(add_methods)
        method.target = method.target.visit(add_methods)

def clean_function(methods, valueset = typeset):
    """
    Cleans the methods using a valueset analysis, and
    the signature of the methods.
    """
    for method in methods:
        all_args = list(itertools.combinations(valueset.VALUES,
                len(method.arguments)))

        allowed = [a for a in all_args if method.allow(a, typeset)]
        allowed_initial = [
                method.initial_values(arg, valueset)
                for arg in allowed]

        # sets of node, method tuples

        def clean_node(node, sources):
            """ Sources is the clean nodes, and the arguments """
            if not sources:
                args = [initial[node.name] for initial in allowed_initial]
                return args, node
            else:
                posible_args, nodes = zip(*sources)
                posible_args = list(zip(*posible_args))
                new_methods = [method for method in node.methods if
                        any(method.evaluate(args, valueset) != valueset.EXTREMUM
                            for args in posible_args)]
                if not new_methods:
                    raise MethodNotValid(methods)
                new_node = model.node(node.name, nodes, new_methods)
                return_values = [new_node.evaluate(args, valueset)
                        for args in posible_args]
                return return_values, new_node

        method.constraint = method.constraint.visit(clean_node)[1]
        method.target     = method.target.visit(clean_node)[1]

    return methods





class MethodNotValid(Exception):
    """ Method is not valid """

