"""
.. currentmodule:: fbml.test

The tests
"""

from fbml.model import Method, Function
from fbml import buildin
from fbml import node, statement, renode

"""
def incr(number):
    number + 1
"""
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

"""
def add_to_all(numbers, incr):
    generate list from [] using number in numbers:
        append(list, (number + incr))

"""
ADD_TO_ALL = statement(
    {'empty' : tuple()},
    renode(
        statement(
            node(buildin.append, {
                'list': node('list'),
                'elem': node(buildin.add, {
                    'a': node('number'),
                    'b': node('incr')
                })
            })
        ),
        ('list', node('empty')), # Reductor
        {'number': node('numbers')}, # Maps
        {'incr': node('incr')} #Variables
    ),
    'add_to_all'
)

"""
# All compiles to the same thing:

def sum_vectors(avector, bvector):
    generate list from [] using a in avector, b in bvector:
        append(list, (a + b))

def sum_vectors(avector, bvector):
    [ a + b | a in avector, b in bvector ]

def sum_vector(avector, bvector):
    avector + bvector

"""
SUM_VECTORS = statement(
    {'empty' : tuple()},
    renode(
        statement(
            node(buildin.append, {
                'list': node('list'),
                'elem': node(buildin.add, {
                    'a': node('a'), 'b': node('b')
                })
            })
        ),
        ('list', node('empty')), # Reductor
        {'a': node('avector'), 'b': node('bvector')}, # Maps
        {} #Variables
    ),
    'sum_vectors'
)

"""
def scalar_product(vector):
    generate scalar from 1 using number in vector:
        scalar * number
"""

SCALAR_PRODUCT = statement(
    {'initial' : 1},
    renode(
        statement(
            node(buildin.mul, {
                'a': node('scalar'),
                'b': node('number')
            })
        ),
        ('scalar', node('initial')), # Reductor
        {'number': node('vector')}, # Maps
        {} #Variables
    ),
    'sum_vectors'
)

"""
def print_stuff(io, a, b, c):
    using io do:
        print(a)
        print(b)
        print(c)

def print_stuff(io, a, b, c):
    generate io form io using item in [a, b, c]:
        io.print(item)

def read_stuff(io):
    using io do:
        o = read()
        write(result)
    result = parse_int(o) + 10
"""
