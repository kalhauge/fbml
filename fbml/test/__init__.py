"""
.. currentmodule:: fbml.test

The tests
"""

from fbml.model import Method, Function
from fbml import buildin
from fbml import node

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
    {'x1': 10},
    [
        Method(
            node(buildin.le,  {'a': node('number'), 'b': node('x1')}),
            node(buildin.mul, {'a': node('number'), 'b': node('x1')})
        ),
        Method(
            node(buildin.gt,  {'a': node('number'), 'b': node('x1')}),
            node('x1')
        )
    ],
    'mul_if_less'
)

# ABS = Function(
#     Method('abs', ['a'],
#         {'c': 0 },
#         node('lt', [node('a'), node('c')]),
#         node('neg',[node('a')])
#         ),
#     Method('abs', ['a'],
#         {'c': 0 },
#         node('ge', [node('a'), node('c')]),
#         node('a')
#         ),
#     )
#
