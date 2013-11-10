"""
.. currentmodule:: fbml.valueset
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

The valueset is the used to execute and verify the models.
"""

from collections.abc import abstractmethod
import itertools

import operator as opr

import logging
L = logging.getLogger(__name__)

def analyse(method, arguments, valueset):
    """ Short analysis tool """
    return method.evaluate(
            tuple(valueset.const(arg) for arg in arguments), valueset)

class ValueSet (object):
    """ ValueSet

        Besides the abstact methods does the Value set also include a parameter
        called :attr:`extremum`, which is the extremum of the analysis.

    """

    @abstractmethod
    def merge(self, other):
        """ Merges the output of a function.  """

    @classmethod
    def allow(cls, constraint):
        """ Returns True or False after looking at the constraint """
        raise NotImplementedError()

    @classmethod
    def apply(cls, method, args_sets):
        """ Applies a function on a set of value """
        raise NotImplementedError()

    @classmethod
    def const(cls, value):
        """
        This methods returns a set containing the

        :param value:
            the value to create the set from.

        :retruns:
            a :class:`ValueSet` in
        """
        raise NotImplementedError()

class FiniteSet(ValueSet, frozenset):
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

    def merge(self, other):
        return self.__class__(self | other)

    @classmethod
    def const(cls, value):
        return cls({value})

    @classmethod
    def allow(cls, constraint):
        truth = constraint and not False in constraint
        L.debug('allow %s -> %s', constraint, truth)
        return truth

    @classmethod
    def apply(cls, method, args_sets):
        #pylint: disable = W0142
        pymethod = cls.method_mapping[method.code]
        def call(args):
            """ Calls the py method """
            retval = pymethod(*args)
            L.debug("%s%s -> %s", pymethod, args, retval)
            return retval
        retval = cls(call(args) for args in itertools.product(*args_sets))
        L.debug("%r%s -> %s", method, args_sets, retval)
        return retval


FiniteSet.extremum = FiniteSet({})


def all_int_int(args):
    if all('Integer' in a for a in args):
        return TypeSet({'Integer'})
    else:
        return TypeSet.extremum

def binnary_int_bool(args):
    if all('Integer' in a for a in args):
        return TypeSet({'Boolean'})
    else:
        return TypeSet.extremum

def all_real_real(args):
    if all('Real' in a for a in args):
        return TypeSet({'Real'})
    else:
        return TypeSet.extremum

def binnary_real_bool(args):
    if all('Real' in a for a in args):
        return TypeSet({'Boolean'})
    else:
        return TypeSet.extremum

def all_bool_bool(args):
    if all('Boolean' in a for a in args):
        return TypeSet({'Boolean'})
    else:
        return TypeSet.extremum

class TypeSet (frozenset, ValueSet):
    """
    A :class:`TypeSet` is used to evaluate the type of
    a method or function.

    The TypeSet annalysis is a under apporximation
    """

    consts = {
            int : {'Integer'},
            float : {'Real'},
            bool : {'Boolean'}
        }

    method_mapping =  {
        'i_neg' : all_int_int,
        'i_add' : all_int_int,
        'i_sub' : all_int_int,
        'i_mul' : all_int_int,
        'i_ge'  : binnary_int_bool,
        'i_lt'  : binnary_int_bool,
        'i_le'  : binnary_int_bool,
        'i_gt'  : binnary_int_bool,
        'i_eq'  : binnary_int_bool,
        'r_neg' : all_real_real,
        'r_add' : all_real_real,
        'r_sub' : all_real_real,
        'r_mul' : all_real_real,
        'r_ge'  : binnary_real_bool,
        'r_lt'  : binnary_real_bool,
        'r_le'  : binnary_real_bool,
        'r_gt'  : binnary_real_bool,
        'r_eq'  : binnary_real_bool,
        'b_not' : all_bool_bool,
        'b_and' : all_bool_bool,

        'boolean' : (lambda x :
            (TypeSet.bool if x[0] >= TypeSet.bool else TypeSet.extremum)),
        'integer' : (lambda x :
            (TypeSet.bool if x[0] >= TypeSet.int else TypeSet.extremum)),
        'real'    : (lambda x :
            (TypeSet.bool if x[0] >= TypeSet.real else TypeSet.extremum))
        }


    def merge(self, other):
        return self.__class__(self | other)

    @classmethod
    def allow(cls, constraint):
        truth = constraint == TypeSet.bool
        L.debug('allow %s -> %s', constraint, truth)
        return truth


    @classmethod
    def const(cls, value):
        return cls(cls.consts[value.__class__])

    @classmethod
    def apply(cls, method, args_sets):
        retval = cls.method_mapping[method.code](args_sets)
        L.debug("%r%s -> %s", method, args_sets, retval)
        return retval

    def __repr__(self):
        return str(set(self)) + hex(hash(self))

TypeSet.extremum = TypeSet({})
TypeSet.int = TypeSet({'Integer'})
TypeSet.real = TypeSet({'Real'})
TypeSet.bool = TypeSet({'Boolean'})



