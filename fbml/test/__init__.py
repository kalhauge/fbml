"""
.. currentmodule:: fbml.test

The tests
"""

from fbml.model import Method, Function
from fbml import buildin
from fbml import node, statement

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
    {'empty' : tuple() }
    renode(
        statement(
            node('append', {
                'list': node('reductor'),
                'elem': node(INCR, {
                    'number': node('number')
                })
            })
        ),
        {'reductor': node('empty')}, # Reductor
        {'number': node('numbers')}, # Maps
        {'increment': node('increment')} #Variables
    ),
    'add_to_all'
)

SUM_VECTORS = statement(
    {'empty' : tuple() }
    renode(
        statement(
            node('append', {
                'list': node('reductor'),
                'elem': node(buildin.add, {
                    'a': node('a'), 'b': node('b')
                })
            })
        ),
        {'reductor': node('empty')}, # Reductor
        {'a': node('avector'), 'b': node('bvector')}, # Maps
        {} #Variables
    ),
    'sum_vectors'
)

SCALAR_PRODUCT = statement(
    {'empty' : tuple() }
    renode(
        statement(
            node('append', {
                'list': node('reductor'),
                'elem': node(buildin.add, {
                    'a': node('a'), 'b': node('b')
                })
            })
        ),
        {'reductor': node('empty')}, # Reductor
        {'a': node('avector'), 'b': node('bvector')}, # Maps
        {} #Variables
    ),
    'sum_vectors'
)

SCALAR_PRODUCT = Function(
    {'test': True, 'one': 1},
    [
        Method(
            node('test'),
            node(buildin.commit, {
                'context': node(buildin.mul, {
                    'a':  node(buildin.map_, {
                        'list': node('avector')
                    }),
                    'b':  node(buildin.reduce, {
                        'initial': node('one')
                    })
                })
            })
        )
    ],
    'scalar_product'
)
