"""
.. currentmodule:: fbml.analysis
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""

import logging
L = logging.getLogger(__name__)

def analyse(method, arguments, valueset):
    """ Short analysis tool """
    return method.evaluate(
            tuple(valueset.const(arg) for arg in arguments), valueset)

