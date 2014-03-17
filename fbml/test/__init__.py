"""
.. currentmodule:: fbml.test

The tests
"""

from fbml.model import Method, Function
from fbml import buildin
from fbml import node, statement, renode

INCR = statement(
    {'value': 1},
    node(buildin.add, {
        'a': node('number'),
        'b': node('value')
    }),
    'incr'
)

MUL_IF_LESS = Function(
    {'const': 10},
    [
        Method(
            node(buildin.lt,  {'a': node('number'), 'b': node('const')}),
            node(buildin.mul, {'a': node('number'), 'b': node('const')})
        ),
        Method(
            node(buildin.ge,  {'a': node('number'), 'b': node('const')}),
            node('number')
        )
    ],
    'mul_if_less'
)

ADD_TO_ALL = statement(
    {'empty' : tuple()},
    renode(
        statement(
            node(buildin.append, {
                'list': node('reductor'),
                'elem': node(buildin.add, {
                    'a': node('number'),
                    'b': node('incr')
                })
            })
        ),
        ('reductor', node('empty')), # Reductor
        {'number': node('numbers')}, # Maps
        {'incr': node('incr')} #Variables
    ),
    'add_to_all'
)

SUM_VECTORS = statement(
    {'empty' : tuple()},
    renode(
        statement(
            node(buildin.append, {
                'list': node('reductor'),
                'elem': node(buildin.add, {
                    'a': node('a'), 'b': node('b')
                })
            })
        ),
        ('reductor', node('empty')), # Reductor
        {'a': node('avector'), 'b': node('bvector')}, # Maps
        {} #Variables
    ),
    'sum_vectors'
)

SCALAR_PRODUCT = statement(
    {'initial' : 1},
    renode(
        statement(
            node(buildin.mul, {
                'a': node('reductor'),
                'b': node('number')
            })
        ),
        ('reductor', node('initial')), # Reductor
        {'number': node('vector')}, # Maps
        {} #Variables
    ),
    'sum_vectors'
)
