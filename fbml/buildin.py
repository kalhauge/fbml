"""
.. currentmodule:: fbml.buildin
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""

import logging
L = logging.getLogger(__name__)

from fbml.model import Method, Node

METHODS = (
    Method('add', ('a', 'b'),
        {},
        Node('and', {
            'a': Node('Integer', {'value': Node('a')}),
            'b': Node('Integer', {'value': Node('b')})
            }),
        'add'
        ),
    Method('sub', ('a', 'b'),
        {},
        Node('and', {
            'a': Node('Integer', {'value': Node('a')}),
            'b': Node('Integer', {'value': Node('b')})
            }),
        'sub'
        ),
    Method('mul', ('a', 'b'),
        {},
        Node('and', {
            'a': Node('Integer', {'value': Node('a')}),
            'b': Node('Integer', {'value': Node('b')})
            }),
        'mul'
        ),
    Method('and', ('a', 'b'),
        {},
        Node('and', {
        'a' : Node('Boolean', {'value': Node('a')}),
        'b' : Node('Boolean', {'value': Node('b')}),
            }),
        'and'
        ),
    Method('ge', ('a', 'b'),
        {},
        Node('and', {
        'a' : Node('Integer', {'value': Node('a')}),
        'b' : Node('Integer', {'value': Node('b')}),
            }),
        'ige'
        ),
    Method('lt', ('a', 'b'),
        {},
        Node('and', {
            'a' : Node('Integer', {'value': Node('a')}),
            'b' : Node('Integer', {'value': Node('b')}),
            }),
        'ilt'
        ),
    Method('le', ('a', 'b'),
        {},
        Node('and', {
            'a' : Node('Integer', {'value': Node('a')}),
            'b' : Node('Integer', {'value': Node('b')}),
            }),
        'ile'
        ),
    Method('gt', ('a', 'b'),
        {},
        Node('and', {
            'a' : Node('Integer', {'value': Node('a')}),
            'b' : Node('Integer', {'value': Node('b')}),
            }),
        'igt'
        ),
    Method('eq', ('a', 'b'),
        {},
        Node('and', {
            'a' : Node('Integer', {'value': Node('a')}),
            'b' : Node('Integer', {'value': Node('b')}),
            }),
        'ieq'
        ),
    Method('neg', ('a',),
        {},
        Node('Integer', {'value': Node('a')}),
        'neg'
        ),
    Method('Boolean', ('value',),
        {'true': True},
        Node('true'),
        'Boolean'
        ),
    Method('Integer', ('value',),
        {'true': True},
        Node('true'),
        'Integer'
        ),
)

