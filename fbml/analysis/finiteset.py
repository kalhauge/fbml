"""
.. currentmodule:: fbml.analysis.finiteset
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
import operator as opr
import itertools

import logging
L = logging.getLogger(__name__)

METHOD_MAPPING = {
    'load': lambda x: x,
    'i_neg':  opr.neg,
    'i_add':  opr.add,
    'i_sub':  opr.sub,
    'i_mul':  opr.mul,
    'i_ge':   opr.ge,
    'i_lt':   opr.lt,
    'i_le':   opr.le,
    'i_gt':   opr.gt,
    'i_eq':   opr.eq,
    'r_neg':  opr.neg,
    'r_add':  opr.add,
    'r_sub':  opr.sub,
    'r_mul':  opr.mul,
    'r_ge':   opr.ge,
    'r_lt':   opr.lt,
    'r_le':   opr.le,
    'r_gt':   opr.gt,
    'r_eq':   opr.eq,
    'b_not':  opr.not_,
    'b_and':  opr.and_,

    'boolean': lambda x: isinstance(x, bool),
    'integer': lambda x: x.__class__ == int,
    'real': lambda x: isinstance(x, float),
}

EXTREMUM = frozenset({})


def merge(first, other):
    """ Merges two finitesets """
    return frozenset(first | other)


def const(value):
    """ Returns a constant set """
    return frozenset({value})


def transform(value):
    return value if isinstance(value, frozenset) else const(value)


def allow(constraint):
    """ Check if a constraint is uphold """
    truth = frozenset({True}) == constraint
    L.debug('allow %s -> %s', constraint, truth)
    return truth


def apply(method, args_sets):
    """ Applies the arg_set of the method """
    #pylint: disable = W0142
    pymethod = METHOD_MAPPING[method.code]

    def call(args):
        """ Calls the py method """
        retval = pymethod(*args)
        L.debug("%s%s -> %s", pymethod, args, retval)
        return retval
    retval = frozenset(call(args) for args in itertools.product(*args_sets))
    L.debug("%r%s -> %s", method, args_sets, retval)
    return retval
