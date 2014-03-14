"""
.. currentmodule:: fbml.analysis

"""

import operator as opr
import itertools
from collections import namedtuple

import logging
L = logging.getLogger(__name__)


def all_is(superset, returnset, elseset):
    """
    Tests if all arguments is a subset of the superset, if it is returnset
    is returned else the EXTREMUM is returned.
    """
    return (lambda args: returnset
            if all(superset >= arg for arg in args)
            else elseset)


def if_subset(typeset, thenset, elseset):
    """
    Creates a function able to test if a tuple containing a single
    set which is a subset of of the typeset argumment.
    """
    return lambda other: thenset if other[0] >= typeset else elseset


def reflex(x):
    return x


class FiniteSet (object):

    METHOD_MAPPING = {
        'load': reflex,
        'i_map': reflex,
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

    @staticmethod
    def merge(first, other):
        """ Merges two finitesets """
        return frozenset(first | other)

    @staticmethod
    def const(value):
        """ Returns a constant set """
        return frozenset({value})

    @classmethod
    def transform(cls, value):
        return value if isinstance(value, frozenset) else cls.const(value)

    @staticmethod
    def allow(constraint):
        """ Check if a constraint is uphold """
        truth = frozenset({True}) == constraint
        L.debug('allow %s -> %s', constraint, truth)
        return truth

    @classmethod
    def apply(cls, method, args_sets):
        """ Applies the arg_set of the method """
        #pylint: disable = W0142
        pymethod = cls.METHOD_MAPPING[method.code]

        def call(args):
            """ Calls the py method """
            retval = pymethod(*args)
            return retval

        retval = frozenset(
            call(args) for args in itertools.product(*args_sets)
        )
        L.debug("%r%s -> %s", method, args_sets, retval)
        return retval


BasicType = namedtuple('BasicType', ['name'])
CombinedType = namedtuple('CombinedType', ['types'])
ListType = namedtuple('ListType', ['type'])


class TypeSet (object):

    integer = BasicType('Integer')
    boolean = BasicType('Boolean')
    real = BasicType('Real')

    INTEGER = frozenset({integer})
    BOOLEAN = frozenset({boolean})
    REAL = frozenset({real})

    INTEGER_LIST = frozenset({ListType(integer)})
    REAL_LIST = frozenset({ListType(real)})
    BOOL_LIST = frozenset({ListType(boolean)})

    EXTREMUM = frozenset({})

    VALUES = (INTEGER, BOOLEAN, REAL)

    CONSTS = {
        int: INTEGER,
        float: REAL,
        bool: BOOLEAN
    }

    METHOD_MAPPING = {
        'load': lambda x: tuple(x)[0],
        'i_map':    all_is(INTEGER_LIST, INTEGER, EXTREMUM),
        'i_neg':    all_is(INTEGER, INTEGER, EXTREMUM),
        'i_add':    all_is(INTEGER, INTEGER, EXTREMUM),
        'i_sub':    all_is(INTEGER, INTEGER, EXTREMUM),
        'i_mul':    all_is(INTEGER, INTEGER, EXTREMUM),
        'i_ge':     all_is(INTEGER, BOOLEAN, EXTREMUM),
        'i_lt':     all_is(INTEGER, BOOLEAN, EXTREMUM),
        'i_le':     all_is(INTEGER, BOOLEAN, EXTREMUM),
        'i_gt':     all_is(INTEGER, BOOLEAN, EXTREMUM),
        'i_eq':     all_is(INTEGER, BOOLEAN, EXTREMUM),

        'r_map':    all_is(REAL_LIST, REAL, EXTREMUM),
        'r_neg':    all_is(REAL,    REAL,    EXTREMUM),
        'r_add':    all_is(REAL,    REAL,    EXTREMUM),
        'r_sub':    all_is(REAL,    REAL,    EXTREMUM),
        'r_mul':    all_is(REAL,    REAL,    EXTREMUM),
        'r_ge':     all_is(REAL,    BOOLEAN, EXTREMUM),
        'r_lt':     all_is(REAL,    BOOLEAN, EXTREMUM),
        'r_le':     all_is(REAL,    BOOLEAN, EXTREMUM),
        'r_gt':     all_is(REAL,    BOOLEAN, EXTREMUM),
        'r_eq':     all_is(REAL,    BOOLEAN, EXTREMUM),

        'b_map':    all_is(REAL_LIST, REAL, EXTREMUM),
        'r_neg':    all_is(REAL,    REAL,    EXTREMUM),
        'b_not':    all_is(BOOLEAN, BOOLEAN, EXTREMUM),
        'b_and':    all_is(BOOLEAN, BOOLEAN, EXTREMUM),
        'boolean':  if_subset(BOOLEAN, BOOLEAN, EXTREMUM),
        'integer':  if_subset(INTEGER, BOOLEAN, EXTREMUM),
        'real':     if_subset(REAL, BOOLEAN, EXTREMUM)
    }

    @classmethod
    def merge(cls, first, other):
        """
        Merges the first and an other set after the use of methods.
        """
        return frozenset(first | other)

    @classmethod
    def allow(cls, constraint):
        """
        Returns wether the constraint is true or not.
        """
        truth = constraint == cls.BOOLEAN
        L.debug('allow %s -> %s', constraint, truth)
        return truth

    @classmethod
    def transform(cls, value):
        return value if isinstance(value, frozenset) else cls.const(value)

    @classmethod
    def const(cls, value):
        """
        :returns: the constant of a value
        """
        return cls.CONSTS[value.__class__]

    @classmethod
    def apply(cls, method, args_sets):
        """
        :returns: the set for applying the method on the arguments.
        """
        retval = cls.METHOD_MAPPING[method.code](args_sets)
        L.debug("%r%s -> %s", method, args_sets, retval)
        return retval
