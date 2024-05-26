import unittest
import math
from cooling_hours import get_cooling_hours, find_indices


class TestCoolingHours(unittest.TestCase):
    PRICE_THRESHOLD = 5.644  # The average system price during 2023 was 56.44 EUR/MWh
    TARGET_COOLING_HOURS = 12
    COOLING_WEEKS = list(range(18,40))
    TEST_PRICE_PER_HOUR = [
         3.621,  2.816,  4.817,  3.862,  2.621,  1.372,  3.218, 10.000,
        15.930,  5.644,  7.361,  8.004,  9.022, 10.255,  9.919, 10.869,
        10.240,  4.470,  5.007,  6.101,  8.201, 16.001, 20.432, 22.642
    ]

    def test_find_indices(self):
        self.assertEqual(
            [0, 1, 2, 3, 4, 5, 6, 9, 17, 18],
            find_indices(self.TEST_PRICE_PER_HOUR, lambda elem: elem <= 5.644)
        )
        self.assertEqual(
            [],
            find_indices(self.TEST_PRICE_PER_HOUR, lambda elem: elem <= 1.000)
        )
        self.assertEqual(
            list(range(24)),
            find_indices(self.TEST_PRICE_PER_HOUR, lambda elem: elem > 0)
        )

    def test_get_cooling_hours_target_hours(self):
        self._do_test_get_cooling_hours(
            self.PRICE_THRESHOLD,
            math.e * self.PRICE_THRESHOLD,
            [0, 1, 2, 3, 4, 5, 6, 9, 10, 17, 18, 19]
        )

    def test_get_cooling_hours_too_cheap(self):
        self._do_test_get_cooling_hours(
            max(self.TEST_PRICE_PER_HOUR),
            2*max(self.TEST_PRICE_PER_HOUR),
            list(range(24))
        )

    def test_get_cooling_hours_too_expensive(self):
        self._do_test_get_cooling_hours(
            min(self.TEST_PRICE_PER_HOUR),
            2*min(self.TEST_PRICE_PER_HOUR),
            [4, 5]
        )

        self._do_test_get_cooling_hours(
            min(self.TEST_PRICE_PER_HOUR)-1.0,
            min(self.TEST_PRICE_PER_HOUR)-0.1,
            []
        )

    def _do_test_get_cooling_hours(self, threshold_0, threshold_1, expected_hours):
        for current_week in list(set(range(54))-set(self.COOLING_WEEKS)):
            self.assertEqual(
                [],
                get_cooling_hours(
                    current_week,
                    self.TEST_PRICE_PER_HOUR,
                    [threshold_0, threshold_1],
                    self.TARGET_COOLING_HOURS,
                    self.COOLING_WEEKS
                )
            )

        for current_week in self.COOLING_WEEKS:
            self.assertEqual(
                expected_hours,
                get_cooling_hours(
                    current_week,
                    self.TEST_PRICE_PER_HOUR,
                    [threshold_0, threshold_1],
                    self.TARGET_COOLING_HOURS,
                    self.COOLING_WEEKS
                )
            )


if __name__ == '__main__':
    unittest.main()
