import unittest
from utils import find_indices


class TestUtils(unittest.TestCase):
    TEST_LST = [
         3.621,  2.816,  4.817,  3.862,  2.621,  1.372,  3.218, 10.000,
        15.930,  5.644,  7.361,  8.004,  9.022, 10.255,  9.919, 10.869,
        10.240,  4.470,  5.007,  6.101,  8.201, 16.001, 20.432, 22.642
    ]

    def test_find_indices(self):
        self.assertEqual(
            [0, 1, 2, 3, 4, 5, 6, 9, 17, 18],
            find_indices(self.TEST_LST, lambda elem: elem <= 5.644)
        )
        self.assertEqual(
            [],
            find_indices(self.TEST_LST, lambda elem: elem <= 1.000)
        )
        self.assertEqual(
            list(range(24)),
            find_indices(self.TEST_LST, lambda elem: elem > 0)
        )


if __name__ == '__main__':
    unittest.main()
