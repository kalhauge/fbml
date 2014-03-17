"""
.. currentmodule:: fbml
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""

import logging
L = logging.getLogger(__name__)

from fbml import model
from fbml import buildin


def node(function, sources=None):
    """ Returns a node

    :param function: A function, or a string indicating which
        source to load

    :param sources: a dict like object
    """
    if not sources and isinstance(function, str):
        return model.Node(buildin.load, [('a', function)])
    else:
        # assert isinstance(function, model.Function)
        return model.Node(function, dict(sources).items())
