"""
.. currentmodule:: fbml.buildin
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""

import logging
L = logging.getLogger(__name__)

from fbml.model import Method, node

BINARY_INTEGER = node('and', [
            node('Integer', [node('a')]),
            node('Integer', [node('b')])
            ])

BINARY_REAL = node('and', [
            node('Real', [node('a')]),
            node('Real', [node('b')])
            ])

UNARY_INTEGER = node('Integer', [node('value')])

UNARY_BOOLEAN = node('Boolean', [node('value')])

UNARY_REAL    = node('Real',    [node('value')])

BINARY_BOOLEAN = node('and', [
            node('Boolean', [node('a')]),
            node('Boolean', [node('b')])
            ])

i_neg = Method('neg', ('a',),     {}, UNARY_INTEGER,  'i_neg'),

i_add = Method('add', ('a', 'b'), {}, BINARY_INTEGER, 'i_add'),
i_sub = Method('sub', ('a', 'b'), {}, BINARY_INTEGER, 'i_sub'),
i_mul = Method('mul', ('a', 'b'), {}, BINARY_INTEGER, 'i_mul'),
i_ge  = Method('ge',  ('a', 'b'), {}, BINARY_INTEGER, 'i_ge'),
i_lt  = Method('lt',  ('a', 'b'), {}, BINARY_INTEGER, 'i_lt'),
i_le  = Method('le',  ('a', 'b'), {}, BINARY_INTEGER, 'i_le'),
i_gt  = Method('gt',  ('a', 'b'), {}, BINARY_INTEGER, 'i_gt'),
i_eq  = Method('eq',  ('a', 'b'), {}, BINARY_INTEGER, 'i_eq'),

r_neg = Method('neg', ('a',),     {}, UNARY_REAL,     'r_neg'),

r_add = Method('add', ('a', 'b'), {}, BINARY_REAL,    'r_add'),
r_sub = Method('sub', ('a', 'b'), {}, BINARY_REAL,    'r_sub'),
r_mul = Method('mul', ('a', 'b'), {}, BINARY_REAL,    'r_mul'),
r_ge  = Method('ge',  ('a', 'b'), {}, BINARY_REAL,    'r_ge'),
r_lt  = Method('lt',  ('a', 'b'), {}, BINARY_REAL,    'r_lt'),
r_le  = Method('le',  ('a', 'b'), {}, BINARY_REAL,    'r_le'),
r_gt  = Method('gt',  ('a', 'b'), {}, BINARY_REAL,    'r_gt'),
r_eq  = Method('eq',  ('a', 'b'), {}, BINARY_REAL,    'r_eq'),

b_not = Method('not', ('a',),     {}, UNARY_BOOLEAN,  'b_not'),
b_and = Method('and', ('a', 'b'), {}, BINARY_BOOLEAN, 'b_and'),

boolean = Method('Boolean', ('value',), {'true': True}, node('true'), 'boolean'),
integer = Method('Integer', ('value',), {'true': True}, node('true'), 'integer'),
real    = Method('Real',    ('value',), {'true': True}, node('true'), 'real'),

METHODS = (
    i_neg,
    i_add,
    i_sub,
    i_mul,
    i_ge ,
    i_lt ,
    i_le ,
    i_gt ,
    i_eq ,
    r_neg,
    r_add,
    r_sub,
    r_mul,
    r_ge ,
    r_lt ,
    r_le ,
    r_gt ,
    r_eq ,
    b_not,
    b_and,
    boolean,
    integer,
    real,
)

