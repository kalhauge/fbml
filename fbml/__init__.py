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


def statement(*args):
    """ Returns a simple function with a single node, that always is run"""
    real_consts = {'test' : True }
    if len(args) == 1:
        s_node = args[0]
        name = None
    elif len(args) == 2:
        s_node, name = args
    else:
        consts, s_node, name = args
        real_consts.update(consts)

    return model.Function(real_consts, [model.Method(node('test'), s_node)], name)

def renode(function, reductor, maps, sources):
    return model.ReductionNode(function, reductor, dict(maps).items(), dict(sources).items())
