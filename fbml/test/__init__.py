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
            node(buildin.add, [node('a'), node('value')])
        )
    ]
)

MUL_IF_LESS = Function(
    {'x1': 10},
    [
        Method(
            node(buildin.le,  [node('number'), node('x1')]),
            node(buildin.mul, [node('number'), node('x1')])
        )
    ]
)

# TAX = Function(
#     {'x1' : 300000.0, 'x3' : 0.40, 'x2' : 0.60 },
#     [
#         Method(
#             node(buildin.le, [node('income'), node('x1')]),
#             node(buildin.mul, [node('income'), node('x3')]),
#             ),
#         Method(
#             node(buildin.gt, [node('income'), node('x1')]),
#             node(buildin.add, [
#                 node(buildin.mul, [
#                     node(buildin.sub,[
#                         node('income'),
#                         node('x1')
#                         ]),
#                     node('x2')
#                     ]),
#                 node(TAX, [node('x1')]),
#                 ])
#             ),
#         ]
#     )

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
