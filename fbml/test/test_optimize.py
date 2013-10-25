"""

.. currentmodule:: fbml.test.test_optimize
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""

from fbml.model import Method, node
from fbml import optimize


def test_taxes():
    """
    This example test the taxes example
    """

    tax = {
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
            )
        }

    optimize.link(tax)

    print(tax)


