"""
.. currentmodule:: fbml.valueset
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

The valueset is the used to execute and verify the models.
"""

from collections.abc import abstractmethod, Set
import itertools

import logging
L = logging.getLogger(__name__)

from fbml.buildin import PY_MEHTODS

class ValueSet (object):
    """
    The ValueSet should contain a

    """

    @abstractmethod
    def union(self, other):
        """
        The union.
        """

    @abstractmethod
    def intersection(self, other):
        """
        The union.

        :param other:

        :returns:
            the intersection in the from of a :class:`ValueSet`
        """

    @abstractmethod
    def subset(self, other):
        """
        :param other:
            an other set of the same type.

        :returns:
            eighter ``True`` or ``False``
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
        L.debug("%s buildin %s %s", method, PY_MEHTODS[method], args_sets)
        return cls(itertools.starmap(
            PY_MEHTODS[method], itertools.product(*args_sets)))


    def __iter__(self):
        return iter(self.inner_set)

    def __len__(self):
        return len(self.inner_set)

    def __contains__(self, elm):
        return elm in self.inner_set

    def __repr__(self):
        return repr(set(self.inner_set))


FiniteSet.min = FiniteSet({})


