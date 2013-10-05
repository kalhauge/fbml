"""
.. currentmodule:: fbml.optimize
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""

import logging
L = logging.getLogger(__name__)

from fbml import model

def visit(basenode, function):
    """
    A visitor for nodes.

    :param basenode:
        The basenode is the lowest node in the graph

    :param function:
        Is the function that for each node returns anything
        . The function must accept a node, and a
        dictionary maping the old nodes to new values::

            function :=  Node, ( Node -> ? ) -> ?

    :returns:
        Whatever the function returns
    """
    mapping = {}
    for node in reversed(basenode.nodes_in_order()):
        mapping[node] = function(node, mapping)
    return mapping[basenode]

def link(methods):
    """
    Links the nodes to the methods
    """
    named_methods = {}
    for method in methods:
        named_methods.setdefault(method.name, []).append(method)

    def add_methods(old_node, sources):
        """
        Add methods to nodes, and returs a new node
        """
        if old_node.sources:
            return model.node(old_node.name,
                    tuple(sources[src] for src in old_node.sources),
                    named_methods[old_node.name])
        else:
            return old_node

    for method in methods:
        method.contraint = visit(method.contraint, add_methods)
        if not method.is_buildin():
            method.target = visit(method.target, add_methods)


def typed(method):
    """
    Removes all wrongly typed methods.
    """
    pass


