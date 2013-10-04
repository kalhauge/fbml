"""
.. currentmodule:: fbml.utils
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
import collections

import logging
L = logging.getLogger(__name__)

class frozendict(collections.Mapping):
    """Don't forget the docstrings!!"""

    def __init__(self, *args, **kwargs):
        self._dict = dict(*args, **kwargs)

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __getitem__(self, key):
        return self._dict[key]

    def __hash__(self):
        return hash(frozenset(self._dict))


