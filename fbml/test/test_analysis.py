"""
.. currentmodule:: fbml.test.test_optimize
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
from nose.tools import assert_equal

from fbml.test import MUL_IF_LESS, INCR
from fbml.analysis import TypeSet, FiniteSet
from fbml import buildin
from fbml.visitor import Cleaner


def test_multiply_finite_set():
    """
    this example test a simple mulitply, tested with FiniteSet
    """
    value = FiniteSet.run(MUL_IF_LESS, number=2)
    assert_equal(value, FiniteSet.const(20))


def test_multiply_type_set():
    """
    this example test a simple mulitply, tested with TypeSet
    """
    value = TypeSet.run(MUL_IF_LESS, number=2)

    assert_equal(value, TypeSet.const(20))
    assert_equal(value, TypeSet.INTEGER)

    value = TypeSet.run(MUL_IF_LESS, number=2.0)
    assert_equal(value, TypeSet.extremum)


def test_incr_type_set_clean():
    """ This example tests the cleaning of INCR"""
    function = Cleaner(TypeSet()).call(INCR, number=10)

    point_of_interest = function.methods[0].statement.function.methods
    assert_equal(point_of_interest, (buildin.i_add,))


def test_multiply_finite_set_clean_gt():
    """
    This example tests cleaning of mul_if_lees if greater that or equal 10
    """
    function = Cleaner(FiniteSet()).call(MUL_IF_LESS, number=10)

    assert_equal(len(function.methods), 1)

    point_of_interest = function.methods[0].statement.function
    assert_equal(point_of_interest.methods, buildin.load.methods)


def test_multiply_finite_set_clean_le():
    """ This example tests the cleaning of multiply, if less than 10"""
    function = Cleaner(FiniteSet()).call(MUL_IF_LESS, number=9)

    assert_equal(len(function.methods), 1)

    point_of_interest = function.methods[0].statement.function
    assert_equal(point_of_interest.methods, buildin.mul.methods)
