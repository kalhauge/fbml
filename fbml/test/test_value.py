"""
TEST
"""

from fbml.value import TypeSet, FiniteValueSet

def test_finite_set():
    assert FiniteValueSet({1, 2}) <= TypeSet(int)
    assert not FiniteValueSet({1, 'st', 2}) <= TypeSet(int)
    assert FiniteValueSet({'st', 'bananna'}) <= TypeSet(str)
    assert TypeSet(int) <= TypeSet(int)
    assert not TypeSet(int) <= FiniteValueSet({1, 2})
