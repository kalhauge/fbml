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

ADD_ONE_TO_ALL = Function(
    {'test': True},
    [
        Method(
            node('test'),
            renode(Function( {'test' : True }, [Method(node('test'), node('append', {'list': node('reductor'), 'elem': node(INCR, 'number':node('number') )
            node(buildin.commit, {
                'context': node(INCR, {
                    'number':  node(buildin.map_, {
                        'list': node('numbers')
                    })
                })
            })
        )
    ],
    'add_one_to_all'
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

SUM_VECTORS = Function(
    {'test': True},
    [
        Method(
            node('test'),
            node(buildin.commit, {
                'context': node(buildin.add, {
                    'a':  node(buildin.map_, {
                        'list': node('avector')
                    }),
                    'b':  node(buildin.map_, {
                        'list': node('bvector')
                    })
                })
            })
        )
    ],
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
