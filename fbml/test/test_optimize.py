"""

.. currentmodule:: fbml.test.test_optimize
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""

from fbml.model import Method, node
from fbml import optimize
from fbml.buildin import METHODS
from fbml.valueset import FiniteSet


def test_multiply():
    """
    this example test a simple mulitply
    """

    mult = (
        Method('multi', ['number'],
            {'x1': 10},
            node('le', [node('number'), node('x1')]),
            node('mul',[node('x1'), node('number')])
            ),
        )

    optimize.link(METHODS + mult)

    value = mult[-1].evaluate((FiniteSet({2, 3}),), FiniteSet)
    print(value)

    assert value == FiniteSet({20, 30})


def test_taxes():
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

    tax = (
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

    optimize.link(METHODS + tax)

    value = tax[-1].evaluate((FiniteSet({300100.0}),), FiniteSet)
    print(value)

    assert value == FiniteSet({120060.0})



