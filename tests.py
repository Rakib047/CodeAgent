# tests.py

import math_ops

def test_square():
    assert math_ops.square(2) == 4
    assert math_ops.square(-3) == 9

def run_tests():
    print "Running tests..."
    test_square()
    print "All tests passed."

if __name__ == "__main__":
    run_tests()


