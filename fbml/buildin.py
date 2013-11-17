"""
.. currentmodule:: fbml.buildin
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
#pylint: disable = C0103

import logging
L = logging.getLogger(__name__)

from fbml.model import BuildInMethod, Function

boolean = BuildInMethod('boolean')
integer = BuildInMethod('integer')
real    = BuildInMethod('real')

b_not = BuildInMethod('b_not')
b_and = BuildInMethod('b_and')

i_neg = BuildInMethod('i_neg')

i_add = BuildInMethod('i_add')
i_sub = BuildInMethod('i_sub')
i_mul = BuildInMethod('i_mul')
i_ge  = BuildInMethod('i_ge')
i_lt  = BuildInMethod('i_lt')
i_le  = BuildInMethod('i_le')
i_gt  = BuildInMethod('i_gt')
i_eq  = BuildInMethod('i_eq')

r_neg = BuildInMethod('r_neg')

r_add = BuildInMethod('r_add')
r_sub = BuildInMethod('r_sub')
r_mul = BuildInMethod('r_mul')
r_ge  = BuildInMethod('r_ge')
r_lt  = BuildInMethod('r_lt')
r_le  = BuildInMethod('r_le')
r_gt  = BuildInMethod('r_gt')
r_eq  = BuildInMethod('r_eq')


load = BuildInMethod('load')

load = Function('load', ('a',),     {}, [load])
not_ = Function('not',  ('a',),     {}, [b_not])
and_ = Function('and',  ('a', 'b'), {}, [b_and])

neg = Function('neg',   ('a', ),    {}, [i_neg, r_neg])

add = Function('add',   ('a', 'b'), {}, [i_add, r_add])
sub = Function('sub',   ('a', 'b'), {}, [i_sub, r_sub])
mul = Function('mul',   ('a', 'b'), {}, [i_mul, r_mul])
ge = Function('ge',     ('a', 'b'), {}, [i_ge, r_ge])
lt = Function('lt',     ('a', 'b'), {}, [i_lt, r_lt])
le = Function('le',     ('a', 'b'), {}, [i_le, r_le])
gt = Function('gt',     ('a', 'b'), {}, [i_gt, r_gt])
eq = Function('eq',     ('a', 'b'), {}, [i_eq, r_eq])



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



