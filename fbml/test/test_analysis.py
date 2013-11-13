"""
.. currentmodule:: fbml.test.test_optimize
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""

from fbml import optimize
from fbml.test import *
from fbml.buildin import METHODS
from fbml.analysis import typeset, finiteset, analyse


def test_multiply_finite_set():
    """
    this example test a simple mulitply, tested with FiniteSet
    """
    optimize.link(METHODS + MUL_IF_LESS)
    value = analyse(MUL_IF_LESS[-1], (2, ), finiteset)
    assert value == finiteset.const(20), str(value)

def test_multiply_type_set():
    """
    this example test a simple mulitply, tested with TypeSet
    """
    optimize.link(METHODS + MUL_IF_LESS)
    value = analyse(MUL_IF_LESS[-1], (2, ), typeset)
    assert value == typeset.INTEGER,  str(value)

    value = analyse(MUL_IF_LESS[-1], (2.0, ), typeset)
    assert value == typeset.EXTREMUM, str(value)

def test_taxes_finite_set():
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
    optimize.link(METHODS + TAX)
    value = analyse(TAX[-1], (300100.0, ), finiteset)
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
    optimize.link(METHODS + TAX)
    value = analyse(TAX[-1], (300100.0, ), typeset)
    assert value == typeset.REAL, str(value)



