"""
.. currentmodule:: fbml.analysis.typeset
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""

import logging
L = logging.getLogger(__name__)


INTEGER  = frozenset({'Integer'})
BOOLEAN  = frozenset({'Boolean'})
REAL     = frozenset({'Real'})
EXTREMUM = frozenset({})

VALUES = (INTEGER, BOOLEAN, REAL)


CONSTS = {
    int   : INTEGER,
    float : REAL,
    bool  : BOOLEAN
}

def all_is(superset, returnset):
    """
    Tests if all arguments is a subset of the superset, if it is returnset is
    returned else the EXTREMUM is returned.
    """
    return (lambda args: returnset
            if all(superset >= arg for arg in args)
            else EXTREMUM)

def if_subset(typeset, thenset, elseset):
    """
    Creates a function able to test if a tuple containing a single
    set which is a subset of of the typeset argumment.
    """
    return lambda other: thenset if other[0] >= typeset else elseset

METHOD_MAPPING =  {
    'i_neg'   : all_is(INTEGER, INTEGER),
    'i_add'   : all_is(INTEGER, INTEGER),
    'i_sub'   : all_is(INTEGER, INTEGER),
    'i_mul'   : all_is(INTEGER, INTEGER),
    'i_ge'    : all_is(INTEGER, BOOLEAN),
    'i_lt'    : all_is(INTEGER, BOOLEAN),
    'i_le'    : all_is(INTEGER, BOOLEAN),
    'i_gt'    : all_is(INTEGER, BOOLEAN),
    'i_eq'    : all_is(INTEGER, BOOLEAN),
    'r_neg'   : all_is(REAL,    REAL),
    'r_add'   : all_is(REAL,    REAL),
    'r_sub'   : all_is(REAL,    REAL),
    'r_mul'   : all_is(REAL,    REAL),
    'r_ge'    : all_is(REAL,    BOOLEAN),
    'r_lt'    : all_is(REAL,    BOOLEAN),
    'r_le'    : all_is(REAL,    BOOLEAN),
    'r_gt'    : all_is(REAL,    BOOLEAN),
    'r_eq'    : all_is(REAL,    BOOLEAN),
    'b_not'   : all_is(BOOLEAN, BOOLEAN),
    'b_and'   : all_is(BOOLEAN, BOOLEAN),
    'boolean' : if_subset(BOOLEAN, BOOLEAN, EXTREMUM),
    'integer' : if_subset(INTEGER, BOOLEAN, EXTREMUM),
    'real'    : if_subset(REAL, BOOLEAN, EXTREMUM)
    }

def merge(first, other):
    """
    Merges the first and an other set after the use of methods.
    """
    return frozenset(first | other)

def allow(constraint):
    """
    Returns wether the constraint is true or not.
    """
    truth = constraint == BOOLEAN
    L.debug('allow %s -> %s', constraint, truth)
    return truth

def const(value):
    """
    :returns: the constant of a value
    """
    return CONSTS[value.__class__]

def apply(method, args_sets):
    """
    :returns: the set for applying the method on the arguments.
    """
    retval = METHOD_MAPPING[method.code](args_sets)
    L.debug("%r%s -> %s", method, args_sets, retval)
    return retval


