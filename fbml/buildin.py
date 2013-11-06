"""
.. currentmodule:: fbml.buildin
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""
import operator as opr
import logging
L = logging.getLogger(__name__)

from fbml.model import BuildInMethod, node

boolean = BuildInMethod('Boolean', ('value',), 'boolean')
integer = BuildInMethod('Integer', ('value',), 'integer')
real    = BuildInMethod('Real',    ('value',), 'real')


b_not = BuildInMethod('not', ('a',),     'b_not')
b_and = BuildInMethod('and', ('a', 'b'), 'b_and')

i_neg = BuildInMethod('neg', ('a',),     'i_neg')

i_add = BuildInMethod('add', ('a', 'b'), 'i_add')
i_sub = BuildInMethod('sub', ('a', 'b'), 'i_sub')
i_mul = BuildInMethod('mul', ('a', 'b'), 'i_mul')
i_ge  = BuildInMethod('ge',  ('a', 'b'), 'i_ge')
i_lt  = BuildInMethod('lt',  ('a', 'b'), 'i_lt')
i_le  = BuildInMethod('le',  ('a', 'b'), 'i_le')
i_gt  = BuildInMethod('gt',  ('a', 'b'), 'i_gt')
i_eq  = BuildInMethod('eq',  ('a', 'b'), 'i_eq')

r_neg = BuildInMethod('neg', ('a',),     'r_neg')

r_add = BuildInMethod('add', ('a', 'b'), 'r_add')
r_sub = BuildInMethod('sub', ('a', 'b'), 'r_sub')
r_mul = BuildInMethod('mul', ('a', 'b'), 'r_mul')
r_ge  = BuildInMethod('ge',  ('a', 'b'), 'r_ge')
r_lt  = BuildInMethod('lt',  ('a', 'b'), 'r_lt')
r_le  = BuildInMethod('le',  ('a', 'b'), 'r_le')
r_gt  = BuildInMethod('gt',  ('a', 'b'), 'r_gt')
r_eq  = BuildInMethod('eq',  ('a', 'b'), 'r_eq')




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


PY_MEHTODS =  {
        i_neg : opr.neg,
        i_add : opr.add,
        i_sub : opr.sub,
        i_mul : opr.mul,
        i_ge  : opr.ge,
        i_lt  : opr.lt ,
        i_le  : opr.le ,
        i_gt  : opr.gt ,
        i_eq  : opr.eq ,
        r_neg : opr.neg,
        r_add : opr.add,
        r_sub : opr.sub,
        r_mul : opr.mul,
        r_ge  : opr.ge ,
        r_lt  : opr.lt ,
        r_le  : opr.le ,
        r_gt  : opr.gt ,
        r_eq  : opr.eq ,
        b_not : opr.not_,
        b_and : opr.and_,

        boolean : lambda x : isinstance(x, bool),
        integer : lambda x : x.__class__ == int,
        real    : lambda x : isinstance(x, float),
        }
