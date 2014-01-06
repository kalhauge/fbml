"""
Optimizations tests

"""

# from nose.tools import assert_equal
#
# from fbml import test
# from fbml import buildin
# from fbml.analysis import typeset
# from fbml.optimize import link, clean_function
#
#
#
# def test_link():
#     """ Test that the linking of MUL_IF_LESS """
#     func = tuple(m.copy() for m in test.MUL_IF_LESS)
#     link(buildin.METHODS + func)
#     method = func[0]
#
#     assert_equal(method.target.methods, (buildin.i_mul, buildin.r_mul))
#     assert_equal(method.constraint.methods, (buildin.i_le, buildin.r_le))
#
# def test_clean():
#     """ Test that the linking of MUL_IF_LESS """
#     func = tuple(m.copy() for m in test.MUL_IF_LESS)
#     link(buildin.METHODS + func)
#     clean_function(func, (typeset.INTEGER,), typeset)
#     method = func[0]
#
#     assert_equal(method.target.methods, (buildin.i_mul,))
#     assert_equal(method.constraint.methods, (buildin.i_le,))
#
#
#
#
#
