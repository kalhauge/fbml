"""
.. currentmodule:: fbml.test.test_optimize
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
from nose.tools import assert_equal

from fbml.test import MUL_IF_LESS, INCR, ADD_ONE_TO_ALL, SUM_VECTORS
from fbml.analysis import TypeSet, FiniteSet, Eval
from fbml import buildin
from fbml.visitor import Cleaner

from unittest import TestCase

class EvalTester(TestCase):

    def test_mul_if_less(self):
        assert_equal(Eval.run(MUL_IF_LESS, number=2), 20)
        assert_equal(Eval.run(MUL_IF_LESS, number=2.0), 20.0)
        assert_equal(Eval.run(MUL_IF_LESS, number=10), 10)

    def test_incr(self):
        assert_equal(Eval.run(INCR, number=2), 3)
        assert_equal(Eval.run(INCR, number=10), 11)

    def test_add_one_to_all_zero(self):
        assert_equal(Eval.run(ADD_ONE_TO_ALL, numbers=tuple()), tuple())

    def test_add_one_to_all_one(self):
        assert_equal(Eval.run(ADD_ONE_TO_ALL, numbers=(1,)), (2, ))

    def test_add_one_to_all_many(self):
        assert_equal(
            Eval.run(ADD_ONE_TO_ALL, numbers=(1, 2, 3, 4, 5, 8, 2)),
            (2, 3, 4, 5, 6, 9, 3)
        )

    def test_sum_vectors_zero(self):
        assert_equal(Eval.run(SUM_VECTORS, avector=tuple(), bvector=tuple()), tuple())

    def test_sum_vectors_one(self):
        assert_equal(Eval.run(SUM_VECTORS, avector=(1,), bvector= (3, )), (4, ))

    def test_sum_vectors_many(self):
        assert_equal(Eval.run(SUM_VECTORS, avector=(1, 2, 3), bvector=(5, 0, -1)), (6, 2, 2))

    def test_sum_vectors_many_real(self):
        assert_equal(Eval.run(SUM_VECTORS, avector=(1.0, 2.0, 3.0), bvector=(5.0, 0.0, -1.0)), (6.0, 2.0, 2.0))

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

    assert_equal(function.free_variables(), {'number'})


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
