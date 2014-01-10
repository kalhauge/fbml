"""
.. currentmodule:: fbml.test

The tests
"""

from fbml.model import Method, Function
from fbml import buildin
from fbml import node, renode

INCR = Function(
    {'test': True, 'value': 1},
    [
        Method(
            node('test'),
            node(buildin.add, {'a': node('number'), 'b': node('value')})
        )
    ],
    'incr'
)

MUL_IF_LESS = Function(
    {'number': 10},
    [
        Method(
            node(buildin.le,  {'a': node('number'), 'b': node('number')}),
            node(buildin.mul, {'a': node('number'), 'b': node('number')})
        ),
        Method(
            node(buildin.gt,  {'a': node('number'), 'b': node('number')}),
            node('number')
        )
    ],
    'mul_if_less'
)

SCALAR_PRODUCT = Function(
    {'test': True},
    [
        Method(
            node('test'),
            renode(
                buildin.add,
                ('b', node('sum_start')),
                {'a': node(
                    buildin.mul,
                    {'a': node('a'), 'b': node('b')}
                )}
            )
        )
    ],
    'scalar_product'
)
