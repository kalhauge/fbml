"""
.. currentmodule:: fbml.test

The tests
"""

from fbml.model import Method, node

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

ABS = (
    Method('abs', ['a'],
        {'c': 0 },
        node('lt', [node('a'), node('c')]),
        node('neg',[node('a')])
        ),
    Method('abs', ['a'],
        {'c': 0 },
        node('ge', [node('a'), node('c')]),
        node('a')
        ),
    )

INCR = (
    Method('abs', ['a'],
        {'test': True, 'value' : 1 },
        node('test'),
        node('add', [node('test'), node('value')]
        )
    ),
)
