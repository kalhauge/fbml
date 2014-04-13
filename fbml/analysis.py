"""
.. currentmodule:: fbml.analysis

"""
import operator as opr
import itertools
from collections import namedtuple

import logging
L = logging.getLogger(__name__)

from fbml import visitor


def reflex(x):
    return x

Reductor = namedtuple('Reductor', ['initial'])
Map = namedtuple('Map', ['size', 'list'])
Context = namedtuple('Context', ['args', 'trace'])


#
# Analysis
#


def all_is(superset, returnset, elseset):
    """
    Tests if all arguments is a subset of the superset, if it is returnset
    is returned else the extremum is returned.
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



BasicType = namedtuple('BasicType', ['name'])
CombinedType = namedtuple('CombinedType', ['types'])
ListType = namedtuple('ListType', ['type'])


class TypeSet (visitor.Evaluator):

    integer = BasicType('Integer')
    boolean = BasicType('Boolean')
    real = BasicType('Real')

    INTEGER = frozenset({integer})
    BOOLEAN = frozenset({boolean})
    REAL = frozenset({real})

    INTEGER_LIST = frozenset({ListType(integer)})
    REAL_LIST = frozenset({ListType(real)})
    BOOL_LIST = frozenset({ListType(boolean)})

    extremum = frozenset({})

    VALUES = (INTEGER, BOOLEAN, REAL)

    CONSTS = {
        int: INTEGER,
        float: REAL,
        bool: BOOLEAN
    }

    METHOD_MAPPING = {
        'load': lambda x: tuple(x)[0],
        'i_map':    all_is(INTEGER_LIST, INTEGER, extremum),
        'i_neg':    all_is(INTEGER, INTEGER, extremum),
        'i_add':    all_is(INTEGER, INTEGER, extremum),
        'i_sub':    all_is(INTEGER, INTEGER, extremum),
        'i_mul':    all_is(INTEGER, INTEGER, extremum),
        'i_ge':     all_is(INTEGER, BOOLEAN, extremum),
        'i_lt':     all_is(INTEGER, BOOLEAN, extremum),
        'i_le':     all_is(INTEGER, BOOLEAN, extremum),
        'i_gt':     all_is(INTEGER, BOOLEAN, extremum),
        'i_eq':     all_is(INTEGER, BOOLEAN, extremum),

        'r_map':    all_is(REAL_LIST, REAL, extremum),
        'r_neg':    all_is(REAL,    REAL,    extremum),
        'r_add':    all_is(REAL,    REAL,    extremum),
        'r_sub':    all_is(REAL,    REAL,    extremum),
        'r_mul':    all_is(REAL,    REAL,    extremum),
        'r_ge':     all_is(REAL,    BOOLEAN, extremum),
        'r_lt':     all_is(REAL,    BOOLEAN, extremum),
        'r_le':     all_is(REAL,    BOOLEAN, extremum),
        'r_gt':     all_is(REAL,    BOOLEAN, extremum),
        'r_eq':     all_is(REAL,    BOOLEAN, extremum),

        'b_map':    all_is(REAL_LIST, REAL, extremum),
        'r_neg':    all_is(REAL,    REAL,    extremum),
        'b_not':    all_is(BOOLEAN, BOOLEAN, extremum),
        'b_and':    all_is(BOOLEAN, BOOLEAN, extremum),
        'boolean':  if_subset(BOOLEAN, BOOLEAN, extremum),
        'integer':  if_subset(INTEGER, BOOLEAN, extremum),
        'real':     if_subset(REAL, BOOLEAN, extremum)
    }

    def call(self, function, **arguments):
        return self.visit_function(function, arguments)

    def merge(self, first, other):
        """
        Merges the first and an other set after the use of methods.
        """
        return frozenset(first | other)

    def allow(self, constraint):
        """
        Returns wether the constraint is true or not.
        """
        truth = constraint == self.BOOLEAN
        L.debug('allow %s -> %s', constraint, truth)
        return truth

    def transform(self, name, value):
        return value if isinstance(value, frozenset) else self.const(value)

    @classmethod
    def const(cls, value):
        """
        :returns: the constant of a value
        """
        return cls.CONSTS[value.__class__]

    def apply(self, method, args_sets):
        """
        :returns: the set for applying the method on the arguments.
        """
        retval = self.METHOD_MAPPING[method.code](args_sets)
        L.debug("%r%s -> %s", method, args_sets, retval)
        return retval
