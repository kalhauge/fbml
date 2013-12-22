"""
.. currentmodule:: fbml.test.test_optimize
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""

from fbml.test import MUL_IF_LESS, TAX, INCR
from fbml.analysis import typeset, finiteset, Evaluator


def test_multiply_finite_set():
    """
    this example test a simple mulitply, tested with FiniteSet
    """
    evaluator = Evaluator(finiteset)
    value = evaluator.evaluate(MUL_IF_LESS, [2])
    assert value == finiteset.const(20), str(value)


def test_multiply_type_set():
    """
    this example test a simple mulitply, tested with TypeSet
    """
    evaluator = Evaluator(typeset)
    value = evaluator.evaluate(MUL_IF_LESS, [2])

    assert value == typeset.INTEGER,  str(value)

    value = evaluator.evaluate(MUL_IF_LESS, [2.0])
    assert value == typeset.EXTREMUM, str(value)


def test_taxes_finite_set():
    """
    This example test the taxes example

    tax (income) {
        income > 300000 ->
            above = income - 300000,
            below = 300000,
            above * 0.60 + tax below.
        income <= 300000 ->
            income * 0.40.
        }
    """
    evaluator = Evaluator(finiteset)
    value = evaluator.evaluate(TAX, [300100.0])
    assert value == finiteset.const(120060.0), str(value)


def test_taxes_type_set():
    """
    This example test the taxes example

    tax {
        (income) income > 300000 ->
            above = income - 300000,
            below = 300000,
            above * 0.60 + tax below.
        (income) income <= 300000 ->
            income * 0.40.
    }
    """
    evaluator = Evaluator(typeset)
    value = evaluator.evaluate(TAX, [300100.0])
    assert value == typeset.REAL, str(value)


def test_incr_type_set_clean():
    """ This example tests the cleaning of INCR"""
    evaluator = Evaluator(typeset)
    function = evaluator.clean_function(INCR, [typeset.INTEGER])

    print(function)
    assert False
