"""
.. currentmodule:: fbml.utils
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""

import logging
L = logging.getLogger(__name__)


def frozendict(*args, **kwargs):
    """ Returns a dictionary that can't be changed """
    return dict(*args, **kwargs)

