"""
.. currentmodule:: fbml.buildin
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""

import logging
L = logging.getLogger(__name__)

from fbml.model import Method, node

METHODS = (
    Method('add', ('a', 'b'),
        {},
        node('and', {
            'a': node('Integer', {'value': node('a')}),
            'b': node('Integer', {'value': node('b')})
            }),
        'add'
        ),
    Method('sub', ('a', 'b'),
        {},
        node('and', {
            'a': node('Integer', {'value': node('a')}),
            'b': node('Integer', {'value': node('b')})
            }),
        'sub'
        ),
    Method('mul', ('a', 'b'),
        {},
        node('and', {
            'a': node('Integer', {'value': node('a')}),
            'b': node('Integer', {'value': node('b')})
            }),
        'mul'
        ),
    Method('and', ('a', 'b'),
        {},
        node('and', {
        'a' : node('Boolean', {'value': node('a')}),
        'b' : node('Boolean', {'value': node('b')}),
            }),
        'and'
        ),
    Method('ge', ('a', 'b'),
        {},
        node('and', {
        'a' : node('Integer', {'value': node('a')}),
        'b' : node('Integer', {'value': node('b')}),
            }),
        'ige'
        ),
    Method('lt', ('a', 'b'),
        {},
        node('and', {
            'a' : node('Integer', {'value': node('a')}),
            'b' : node('Integer', {'value': node('b')}),
            }),
        'ilt'
        ),
    Method('le', ('a', 'b'),
        {},
        node('and', {
            'a' : node('Integer', {'value': node('a')}),
            'b' : node('Integer', {'value': node('b')}),
            }),
        'ile'
        ),
    Method('gt', ('a', 'b'),
        {},
        node('and', {
            'a' : node('Integer', {'value': node('a')}),
            'b' : node('Integer', {'value': node('b')}),
            }),
        'igt'
        ),
    Method('eq', ('a', 'b'),
        {},
        node('and', {
            'a' : node('Integer', {'value': node('a')}),
            'b' : node('Integer', {'value': node('b')}),
            }),
        'ieq'
        ),
    Method('neg', ('a',),
        {},
        node('Integer', {'value': node('a')}),
        'neg'
        ),
    Method('Boolean', ('value',),
        {'true': True},
        node('true'),
        'Boolean'
        ),
    Method('Integer', ('value',),
        {'true': True},
        node('true'),
        'Integer'
        ),
)

