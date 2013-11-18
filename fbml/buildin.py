"""
.. currentmodule:: fbml.buildin
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
#pylint: disable = C0103

import logging
L = logging.getLogger(__name__)

from fbml.model import BuildInMethod, Function

#boolean = BuildInMethod('boolean')
#integer = BuildInMethod('integer')
#real    = BuildInMethod(('value'), 'real')

b_not = BuildInMethod(('a'),'b_not')
b_and = BuildInMethod(('a', 'b'), 'b_and')

i_neg = BuildInMethod(('a'), 'i_neg')

i_add = BuildInMethod(('a', 'b'), 'i_add')
i_sub = BuildInMethod(('a', 'b'), 'i_sub')
i_mul = BuildInMethod(('a', 'b'), 'i_mul')
i_ge  = BuildInMethod(('a', 'b'), 'i_ge')
i_lt  = BuildInMethod(('a', 'b'), 'i_lt')
i_le  = BuildInMethod(('a', 'b'), 'i_le')
i_gt  = BuildInMethod(('a', 'b'), 'i_gt')
i_eq  = BuildInMethod(('a', 'b'), 'i_eq')

r_neg = BuildInMethod(('a'), 'r_neg')

r_add = BuildInMethod(('a', 'b'), 'r_add')
r_sub = BuildInMethod(('a', 'b'), 'r_sub')
r_mul = BuildInMethod(('a', 'b'), 'r_mul')
r_ge  = BuildInMethod(('a', 'b'), 'r_ge')
r_lt  = BuildInMethod(('a', 'b'), 'r_lt')
r_le  = BuildInMethod(('a', 'b'), 'r_le')
r_gt  = BuildInMethod(('a', 'b'), 'r_gt')
r_eq  = BuildInMethod(('a', 'b'), 'r_eq')


load = BuildInMethod(('a'), 'load')

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
#    boolean,
#    integer,
#    real,
)



