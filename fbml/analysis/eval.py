"""
The eval submodule

"""
import operator as opr
import itertools

import logging
L = logging.getLogger(__name__)

from fbml import visitor

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
    'append': lambda l, a: l + (a,),

    'boolean': lambda x: isinstance(x, bool),
    'integer': lambda x: x.__class__ == int,
    'real': lambda x: isinstance(x, float),
}


class Eval(visitor.Evaluator):
    """
    This is the defacto evaluator, everything that this does is right,
    everything else must follow its example. This eval function can therefor be
    used to see if analysis is infact over or under approximations, and if
    other implmenations is correct.
    """

    extremum = None

    def transform(sel, name, value):
        """ Read the values as is """
        return value

    def merge_all(self, results):
        """ Short surcuit on the results, takes first real result"""
        for result in results:
            if not self.failed(result):
                break
        else:
            result = self.extremum
        return result

    def allow(self, test):
        return test is True

    def apply(self, method, args):
        pymethod = METHOD_MAPPING[method.code]
        return pymethod(*args)


class FiniteSet (visitor.Evaluator):
    """
    Allows for analysing multible numbers at once
    """

    extremum = set()

    @classmethod
    def const(cls, value):
        """ Returns a constant set """
        return {value}

    def transform(self, name, value):
        return value if isinstance(value, set) else self.const(value)

    def merge(self, first, other):
        """ Merges two finitesets """
        return first | other

    def allow(self, constraint):
        """ Check if a constraint is uphold """
        truth = {True} == constraint
        L.debug('allow %s -> %s', constraint, truth)
        return truth

    def apply(self, method, args_sets):
        """ Applies the arg_set of the method """
        pymethod = METHOD_MAPPING[method.code]

        def call(args):
            """ Calls the py method """
            retval = pymethod(*args)
            return retval

        retval = set(call(args) for args in itertools.product(*args_sets))
        L.debug("%r%s -> %s", method, args_sets, retval)
        return retval

class Constraint (visitor.Evaluator):

    """
    This class would use a constraint solver to see if everything is reachabel.
    """



