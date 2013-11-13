"""
Optimizations tests

"""

from nose.tools import assert_equal

from fbml.test import MUL_IF_LESS
from fbml import buildin
from fbml.optimize import link, clean_function



def test_link():
    """ Test that the linking of MUL_IF_LESS """
    link(buildin.METHODS + MUL_IF_LESS)
    method = MUL_IF_LESS[0]

    assert_equal(method.target.methods, (buildin.i_mul, buildin.r_mul))
    assert_equal(method.constraint.methods, (buildin.i_le, buildin.r_le))

def test_clean():
    """ Test that the linking of MUL_IF_LESS """
    link(buildin.METHODS + MUL_IF_LESS)
    clean_function(MUL_IF_LESS)
    method = MUL_IF_LESS[0]

    assert_equal(method.target.methods, (buildin.i_mul,))
    assert_equal(method.constraint.methods, (buildin.i_le,))





