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

UNARY_INTEGER = node('Integer', [node('value')])

BINARY_BOOLEAN = node('and', [
            node('Boolean', [node('a')]),
            node('Boolean', [node('b')])
            ])

METHODS = (
    Method('add', ('a', 'b'), {}, BINARY_INTEGER, 'add'),
    Method('sub', ('a', 'b'), {}, BINARY_INTEGER, 'sub'),
    Method('mul', ('a', 'b'), {}, BINARY_INTEGER, 'mul'),
    Method('ge',  ('a', 'b'), {}, BINARY_INTEGER, 'ige'),
    Method('lt',  ('a', 'b'), {}, BINARY_INTEGER, 'ilt'),
    Method('le',  ('a', 'b'), {}, BINARY_INTEGER, 'ile'),
    Method('gt',  ('a', 'b'), {}, BINARY_INTEGER, 'igt'),
    Method('eq',  ('a', 'b'), {}, BINARY_INTEGER, 'ieq'),
    Method('neg', ('a',),     {}, UNARY_INTEGER,  'neg'),
    Method('and', ('a', 'b'), {}, BINARY_BOOLEAN, 'and'),
    Method('Boolean', ('value',), {'true': True}, node('true'), 'Boolean'),
    Method('Integer', ('value',), {'true': True}, node('true'), 'Integer'),
)

