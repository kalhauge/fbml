"""
.. currentmodule:: fbml.valueset
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

The valueset is the used to execute and verify the models.
"""

from collections.abc import abstractmethod, Set
import itertools

import operator as opr

import logging
L = logging.getLogger(__name__)

class ValueSet (object):
    """ ValueSet """

    @abstractmethod
    def merge(self, other):
        """
        Merges the output of a function. This is often
        seen as the union on under approximations, and
        the intersection in over approximations
        """

    @classmethod
    def apply(cls, method, args_sets):
        """
        Applies a function on a set of value
        """

    @classmethod
    def const(cls, value):
        """
        This methods returns a set containing the

        :param value:
            the value to create the set from.

        :retruns:
            a :class:`ValueSet` in
        """
        return cls(value)

class FiniteSet(ValueSet, Set):
    """
    Finite set is the simplest implementation of ValueSet, but
    is at most situations hopelessly ineffective
    """

    method_mapping =  {
        'i_neg' : opr.neg,
        'i_add' : opr.add,
        'i_sub' : opr.sub,
        'i_mul' : opr.mul,
        'i_ge'  : opr.ge,
        'i_lt'  : opr.lt ,
        'i_le'  : opr.le ,
        'i_gt'  : opr.gt ,
        'i_eq'  : opr.eq ,
        'r_neg' : opr.neg,
        'r_add' : opr.add,
        'r_sub' : opr.sub,
        'r_mul' : opr.mul,
        'r_ge'  : opr.ge ,
        'r_lt'  : opr.lt ,
        'r_le'  : opr.le ,
        'r_gt'  : opr.gt ,
        'r_eq'  : opr.eq ,
        'b_not' : opr.not_,
        'b_and' : opr.and_,

        'boolean' : lambda x : isinstance(x, bool),
        'integer' : lambda x : x.__class__ == int,
        'real'    : lambda x : isinstance(x, float),
        }


    def __init__(self, start_set):
        self.inner_set = frozenset(start_set)

    def union(self, other):
        return self | other

    def intersection(self, other):
        return self & other

    def subset(self, other):
        return self <= other

    @classmethod
    def const(cls, value):
        return cls({value})

    @classmethod
    def apply(cls, method, args_sets):
        pymethod = cls.method_mapping[method.name]
        def call(args):
            """ Calls the py method """
            retval = pymethod(*args)
            L.debug("%s%s -> %s", pymethod, args, retval)
            return retval
        retval = cls(call(args) for args in itertools.product(*args_sets))
        L.debug("%r%s -> %s", method, args_sets, retval)
        return retval

    def __iter__(self):
        return iter(self.inner_set)

    def __len__(self):
        return len(self.inner_set)

    def __contains__(self, elm):
        return elm in self.inner_set

    def __repr__(self):
        return repr(set(self.inner_set))


FiniteSet.min = FiniteSet({})


