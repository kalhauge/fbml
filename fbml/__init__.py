"""
.. currentmodule:: fbml
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""

import logging
L = logging.getLogger(__name__)

from fbml import model
from fbml import buildin


def node(function, sources=None):
    """ Returns a node """
    if not sources and isinstance(function, str):
        return model.Node(buildin.load, ('a', function))
    else:
        return model.Node(function, sources.items())


def renode(function, reduction, sources):
    return model.ReduceNode(
        function,
        reduction,
        tuple(sources),
        tuple(sources.values())
    )
