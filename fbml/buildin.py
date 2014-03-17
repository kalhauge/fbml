"""
.. currentmodule:: fbml.buildin
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
#pylint: disable = C0103

import logging
L = logging.getLogger(__name__)

from fbml.model import BuildInMethod, Function


b_not = BuildInMethod(('a', ), 'b_not')
b_and = BuildInMethod(('a', 'b'), 'b_and')

i_neg = BuildInMethod(('a', ), 'i_neg')

i_add = BuildInMethod(('a', 'b'), 'i_add')
i_sub = BuildInMethod(('a', 'b'), 'i_sub')
i_mul = BuildInMethod(('a', 'b'), 'i_mul')
i_ge = BuildInMethod(('a', 'b'), 'i_ge')
i_lt = BuildInMethod(('a', 'b'), 'i_lt')
i_le = BuildInMethod(('a', 'b'), 'i_le')
i_gt = BuildInMethod(('a', 'b'), 'i_gt')
i_eq = BuildInMethod(('a', 'b'), 'i_eq')

r_neg = BuildInMethod(('a', ), 'r_neg')

r_add = BuildInMethod(('a', 'b'), 'r_add')
r_sub = BuildInMethod(('a', 'b'), 'r_sub')
r_mul = BuildInMethod(('a', 'b'), 'r_mul')
r_ge = BuildInMethod(('a', 'b'), 'r_ge')
r_lt = BuildInMethod(('a', 'b'), 'r_lt')
r_le = BuildInMethod(('a', 'b'), 'r_le')
r_gt = BuildInMethod(('a', 'b'), 'r_gt')
r_eq = BuildInMethod(('a', 'b'), 'r_eq')

load = BuildInMethod(('a', ), 'load')

#i_map = BuildInMethod(('a', ), 'i_map')
#r_map = BuildInMethod(('a', ), 'r_map')

m_map = BuildInMethod(('list', ), 'map')
map_ = Function({}, [m_map], 'map')

m_commit = BuildInMethod(('context',), 'commit')
commit = Function({}, [m_commit], 'commit')

m_reduce= BuildInMethod(('initial',), 'reduce')
reduce = Function({}, [m_context], 'reduce')

load = Function({}, [load], 'load')
not_ = Function({}, [b_not], 'not')
and_ = Function({}, [b_and], 'and')

neg = Function({}, [i_neg, r_neg], 'neg')

add = Function({}, [i_add, r_add], 'add')
sub = Function({}, [i_sub, r_sub], 'sub')
mul = Function({}, [i_mul, r_mul], 'mul')
ge = Function({},  [i_ge, r_ge], 'ge')
lt = Function({},  [i_lt, r_lt], 'lt')
le = Function({},  [i_le, r_le], 'le')
gt = Function({},  [i_gt, r_gt], 'gt')
eq = Function({},  [i_eq, r_eq], 'eq')

METHODS = (
    i_neg,
    i_add,
    i_sub,
    i_mul,
    i_ge,
    i_lt,
    i_le,
    i_gt,
    i_eq,
    r_neg,
    r_add,
    r_sub,
    r_mul,
    r_ge,
    r_lt,
    r_le,
    r_gt,
    r_eq,
    b_not,
    b_and,
)
