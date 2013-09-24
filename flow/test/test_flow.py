"""

Testing that the parser is working correctly

"""
from flow import parse

def test_add():
    """
    Ensures that the simple program add, can be parsed.
    """
    program = """
    method my_add (a : N, b : N)
        c = add(a, b);
    return c
    """
    parse(program)

def test_map_add():
    """
    Ensures that a mapping add, can be parsed.
    """
    program = """
    method my_mapping_add(a : N{X}, b : N{X})
        c = add(map(a), map(b));
    return c
    """
    parse(program)

def test_factorial():
    """
    Ensures that the a factorial program cna be parsed.
    """
    program = """
    method factorial (a : { x > 0 | x : N })
        fact = mult(induct(1),range(1,a));
    return fact
    """
    parse(program)

def test_fibonati():
    """
    Ensures that a fibonati program is parsabel.
    """
    program = """
    method fibonati (before : N, last : N)
        fib = before + last
    return fib

    method fibonati (number : N)
        n = induct([1,1],range(N));
        f_n = fibonati(n); # Not recursion
    return f_n
    """
    parse(program)

