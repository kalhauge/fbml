"""

.. currentmodule:: fbml.test.test_optimize
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""

from fbml.model import Method, node
from fbml import optimize
from fbml.buildin import METHODS
from fbml.valueset import FiniteSet,  analyse
from fbml.analysis import typeset

TAX = (
    Method('tax', ['income'],
        {'x1' : 300000.0, 'x3' : 0.40},
        node('le', [node('income'), node('x1')]),
        node('mul', [node('income'), node('x3')]),
        ),
    Method('tax', ['income'],
        {'x1' : 300000.0, 'x2' : 0.60},
        node('gt', [node('income'), node('x1')]),
        node('add',[
            node('mul', [
                node('sub',[
                    node('income'),
                    node('x1')
                    ]),
                node('x2')
                ]),
            node('tax', [node('x1')]),
            ])
        ),
    Method('main', ['income'],
        {},
        node('Real', [node('income')]),
        node('tax', [node('income')])
        )
    )

MUL_IF_LESS = (
    Method('multi', ['number'],
        {'x1': 10},
        node('le', [node('number'), node('x1')]),
        node('mul',[node('x1'), node('number')])
        ),
    )


def test_multiply_finite_set():
    """
    this example test a simple mulitply, tested with FiniteSet
    """
    optimize.link(METHODS + MUL_IF_LESS)
    value = analyse(MUL_IF_LESS[-1], (2, ), FiniteSet)
    assert value == FiniteSet.const(20), str(value)

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
    value = analyse(TAX[-1], (300100.0, ), FiniteSet)
    assert value == FiniteSet.const(120060.0), str(value)

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
    value = analyse(TAX[-1], (300100.0, ), TypeSet)
    assert False
    assert value == TypeSet({'Real'}), str(value)



