"""
Tests the backend module

"""
from fbml import test
from fbml.backend import llvm_
from fbml.analysis import TypeSet


def compile_function(function, args):
    """ Compiles a function using LLVM """
    function = function.clean(TypeSet, args)
    back = llvm_.LLVMBackend()
    llvm_function = back.compile(function, args)
    print(llvm_function)
    return llvm_function


def test_increment():
    """ Test INCR """
    result = compile_function(test.INCR, {'number': TypeSet.INTEGER})
    assert False, str(result)
    #assert str(result) == '', str(result)

#def est_abs():
#    """
#    Test ABS
#    """
#    func = tuple(m.copy() for m in test.ABS)
#    link(METHODS + func)
#    clean_function(func)
#    back = backend.LLVMBackend()
#    print(back.function_from_methods(func))
#    # assert False
#
# def est_clamp():
#     """
#     Tree methods with multible conditions::
#
#         method clamp
#             a <= high, a >= low
#         procedure
#         end a
#
#         method clamp
#             a > high
#         procedure
#         end high
#
#         method clamp
#             a < low
#         procedure
#         end low
#
#     """
#     high, low, node_a = node('high'), node('low'), node('a')
#
#     clamp_middle = Method('clamp',
#             ('a', 'low', 'high'),
#             {},
#             node('and',(
#                 node('le', (node_a, high) ),
#                 node('ge', (node_a, low) )
#             )),
#             node('a')
#             )
#
#     clamp_high = Method('clamp',
#             ('a', 'low', 'high'),
#             {},
#             node('lt', (node_a, high)),
#             node('high')
#             )
#
#     clamp_low = Method('clamp',
#             ('a', 'low', 'high'),
#             {},
#             node('gt', (node_a, low) ),
#             node('low'))
#
#     methods = METHODS + (clamp_middle, clamp_high, clamp_low)
#     link(methods)
#     back = backend.LLVMBackend()
#     func = back.function_from_methods(
#         [clamp_middle, clamp_high, clamp_low])
#     print(func)
#
# FACTORIAL = (
#     Method('factorial',
#         ('a', ),
#         {'one': 1},
#         node('and', [
#             node('eq', [node('a'), node('one')] ),
#             node('Integer', [node('a')] ),
#             ]),
#         node('a')
#         ),
#     Method('factorial',
#         ('a', ),
#         {'one': 1},
#         node('and', [
#             node('gt', [node('a'), node('one')]),
#             node('Integer', [node('a')]),
#             ]),
#         node('mul', [
#             node('factorial', [
#                 node('sub', [node('a'), node('one')]),
#                 ]),
#             node('a')
#             ])
#         ),
# )
#
# def est_factorial():
#     """
#     Test the output of::
#
#         method factorial
#             a == 1, a : Z
#         procedure
#         end a
#
#         method factorial
#             a > 1, a : Z
#         procedure
#             b = factorial(a - 1) * a
#         end b
#
#     """
#     methods = METHODS + FACTORIAL
#     link(methods)
#     back = backend.LLVMBackend()
#     func = back.function_from_methods(FACTORIAL)
#     print(str(func))
#
# def est_deep_call():
#     """
#     Test the output of::
#
#         method factorial_test
#             a : Z
#         procedure
#             b = factorial(a)
#         end b
#     """
#     method = ( Method('factorial_test', ['a'],
#                     {},
#                     node('Integer',[node('a')]),
#                     node('factorial', [node('a')])
#                     ), )
#
#     methods = METHODS + FACTORIAL + method
#     link(methods)
#     compiler = backend.LLVMBackend()
#     compiler.function_from_methods(method)
#
#     print(compiler.module)
#     compiler.module.verify()
#
# def est_real():
#     """
#     Test the output of::
#
#         method real_add
#             a : R, b : R
#         procedure
#             c = a + b
#         end c
#     """
#     method = (
#             Method('real_add', ['a'], {},
#                 node('and', [
#                     node('Real', [node('a')]),
#                     node('Real', [node('b')])
#                     ]),
#                 node('add', [node('a'), node('b')] )
#                 ),
#             )
#     methods = METHODS + method
#     link(methods)
#     compiler = backend.LLVMBackend()
#     compiler.function_from_methods(method)
#
#     print(compiler.module)
#     compiler.module.verify()
#
