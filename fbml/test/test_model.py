"""

Tests of fbml.model

"""

from fbml.test import INCR


def test_print():
    return None
#     assert str(INCR) == """Function(
#     {'test': True, 'value': 1},
#     [Method(
#         Node('test', None, None),
#         Node(
#             Function(
#                 {},
#                 [BuildInMethod(argmap=('a', 'b'), code='i_add'), BuildInMethod(argmap=('a', 'b'), code='r_add')]
#             ),
#             (
#                 Node('value', None, None),
#                 Node('a', None, None)
#             ),
#             ('b', 'a')
#         )
#     )]
# )
# """, str(INCR)
