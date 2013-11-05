"""
.. currentmodule:: fbml.optimize
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""

import logging
L = logging.getLogger(__name__)

from fbml import model

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

    for method in methods:
        if not method.is_buildin:
            method.contraint = method.contraint.visit(add_methods)
            method.target = method.target.visit(add_methods)

class MethodNotValid(Exception):
    """ Method is not valid """

#def verify(method, valueset):
#    """
#    Verifies a fbml method, and esures that errors are imposible.
#    The method is in all simplicity executed with the valueset.
#
#    :param valueset:
#        This is a namedtuple containing a::
#            union  -> ( S x S ) -> S
#            subset -> ( S x S ) -> {true,false}
#            max    -> S
#            min    -> S
#            const  -> Value -> S
#            apply  -> ( Method x S**?) -> S
#
#    :raises:
#        A MethodNotVailid
#    """
#
#    arg_set = predict_argsets()
#
#    return False
#
#
#def optimize(method):
#    """
#    Optimizes the fbml graph, by removing unreachable methods from
#    nodes, and inline single methods.
#
#    :param method:
#        the method to optimize.
#
#    :returns: the optimized method.
#    """
#
#    return method
#
#
