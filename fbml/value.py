"""
.. currentmodule:: fbml.value
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
import collections.abc

import logging
L = logging.getLogger(__name__)

class ValueSet(object):
    """
    A ValueSet is a set of sets, which is recursively searched though
    if somthing is to be validated.
    """

    def __init__(self, iterator):
        self.subsets = []
        for i in iterator:
            self.add(i)

    def add(self, subset):
        new_set = []
        for test in self.subsets:
            if subset <= test:
                break
            elif not test <= subset:
                new_set.append(test)
        else:
            new_set.append(subset)
        self.subsets = new_set

    def __le__(self, other):
        return all(other <= test for test in self.subsets)

    def __contains__(self, value):
        return any(value in test for test in self.subsets)


class FiniteValueSet(object):

    def __init__(self, values):
        self.values = frozenset(values)

    def __le__(self, other):
        return all(value in other for value in self.values)

    def __contains__(self, value):
        return value in self.values

    def __iter__(self):
        return iter(self.values)

class TypeSet(object):

    def __init__(self, type_):
        self.type = type_

    def __contains__(self, elem):
        return isinstance(elem, self.type)

    def __le__(self, other):
        if isinstance(other, TypeSet):
            return self.type == other.type

def singleton(value):
    return FiniteValueSet((value,))

def union(first, second):
    return ValueSet([first, second])

INTEGERS = TypeSet(int)
