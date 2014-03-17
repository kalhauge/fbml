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

def statement(s_node, name=None, consts={}):
    """ Returns a simple function with a single node, that always is run"""
    real_consts = {'test' : True }
    real_consts.update(consts)
    return Function(consts, [Method(node('test'), s_node)], name)

