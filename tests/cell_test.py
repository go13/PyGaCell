import unittest

from src.cell import Cell
from src.ga import Params


def fn(x):
    return 1


class TestCell(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_cross(self):
        params = Params(3, 2, fn, 3, 1)

        m = Cell.create(params)
        f = Cell.create(params)

        child = Cell.cross(params, m, f)
        child.mutate()

        child.calc([1, 2, 3])

if __name__ == '__main__':
    unittest.main()
