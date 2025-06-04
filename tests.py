# tests.py

import unittest
import math_ops

class TestMathOps(unittest.TestCase):

    def test_square(self):
        self.assertEqual(math_ops.square(2), 4)
        self.assertEqual(math_ops.square(-3), 9)

if __name__ == "__main__":
    unittest.main()
