"""
.. currentmodule:: fbml.test.test_optimize
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""

from fbml.test import MUL_IF_LESS, INCR
from fbml.analysis import TypeSet, FiniteSet
from fbml import buildin


def test_multiply_finite_set():
    """
    this example test a simple mulitply, tested with FiniteSet
    """
    value = MUL_IF_LESS.evaluate(FiniteSet, {'number': 2})
    assert value == FiniteSet.const(20), str(value)


def test_multiply_type_set():
    """
    this example test a simple mulitply, tested with TypeSet
    """
    value = MUL_IF_LESS.evaluate(TypeSet, {'number': 2})

    assert value == TypeSet.const(20), str(value)
    assert value == TypeSet.INTEGER,  str(value)

    value = MUL_IF_LESS.evaluate(TypeSet, {'number': 2.0})
    assert value == TypeSet.EXTREMUM, str(value)


def test_incr_type_set_clean():
    """ This example tests the cleaning of INCR"""
    function = INCR.clean(TypeSet, {'number': 10})

    point_of_interest = function.methods[0].statement.function.methods
    assert point_of_interest == [buildin.i_add]


def test_multiply_finite_set_clean_gt():
    """ This example tests cleaning of mul_if_lees if greater that 10"""
    function = MUL_IF_LESS.clean(FiniteSet, {'number': 11})

    assert len(function.methods) == 1

    point_of_interest = function.methods[0].statement.function
    assert point_of_interest.methods == buildin.load.methods


def test_multiply_finite_set_clean_le():
    """ This example tests the cleaning of multiply, if less or equal to 10"""
    function = MUL_IF_LESS.clean(FiniteSet, {'number': 10})

    assert len(function.methods) == 1

    point_of_interest = function.methods[0].statement.function
    assert point_of_interest.methods == buildin.mul.methods
