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

UNARY_REAL    = node('Real',    [node('value')])

BINARY_BOOLEAN = node('and', [
            node('Boolean', [node('a')]),
            node('Boolean', [node('b')])
            ])

METHODS = (
    Method('neg', ('a',),     {}, UNARY_INTEGER,  'i_neg'),

    Method('add', ('a', 'b'), {}, BINARY_INTEGER, 'i_add'),
    Method('sub', ('a', 'b'), {}, BINARY_INTEGER, 'i_sub'),
    Method('mul', ('a', 'b'), {}, BINARY_INTEGER, 'i_mul'),
    Method('ge',  ('a', 'b'), {}, BINARY_INTEGER, 'i_ge'),
    Method('lt',  ('a', 'b'), {}, BINARY_INTEGER, 'i_lt'),
    Method('le',  ('a', 'b'), {}, BINARY_INTEGER, 'i_le'),
    Method('gt',  ('a', 'b'), {}, BINARY_INTEGER, 'i_gt'),
    Method('eq',  ('a', 'b'), {}, BINARY_INTEGER, 'i_eq'),

    Method('neg', ('a',),     {}, UNARY_REAL,  'r_neg'),

    Method('add', ('a', 'b'), {}, BINARY_REAL,    'r_add'),
    Method('sub', ('a', 'b'), {}, BINARY_REAL,    'r_sub'),
    Method('mul', ('a', 'b'), {}, BINARY_REAL,    'r_mul'),
    Method('ge',  ('a', 'b'), {}, BINARY_REAL,    'r_ge'),
    Method('lt',  ('a', 'b'), {}, BINARY_REAL,    'r_lt'),
    Method('le',  ('a', 'b'), {}, BINARY_REAL,    'r_le'),
    Method('gt',  ('a', 'b'), {}, BINARY_REAL,    'r_gt'),
    Method('eq',  ('a', 'b'), {}, BINARY_REAL,    'r_eq'),

    Method('neg', ('a',),     {}, UNARY_INTEGER,  'neg'),

    Method('and', ('a', 'b'), {}, BINARY_BOOLEAN, 'and'),

    Method('Boolean', ('value',), {'true': True}, node('true'), 'Boolean'),
    Method('Integer', ('value',), {'true': True}, node('true'), 'Integer'),
    Method('Real',    ('value',), {'true': True}, node('true'), 'Real'),
)

