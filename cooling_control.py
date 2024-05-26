import math
import datetime
from utils import find_indices

class CoolingController():
    def __init__(self, price_thresholds, num_target_hours, cooling_weeks):
        self._price_thresholds = price_thresholds
        self._num_target_hours = num_target_hours
        self._cooling_weeks = cooling_weeks

    def get_cooling_hours(self, current_week, prices_per_hour):
        if current_week not in self._cooling_weeks:
            return []
        
        cooling_hours = find_indices(
            prices_per_hour,
            lambda elem: elem <= self._price_thresholds[0]
        )
        if len(cooling_hours) < self._num_target_hours:
            candidate_hours = find_indices(
                prices_per_hour,
                lambda elem: elem > self._price_thresholds[0] and elem <= self._price_thresholds[1]
            )
            hours_to_add = sorted(
                [(hour, prices_per_hour[hour]) for hour in candidate_hours],
                key=lambda elem: elem[1]
            )[:self._num_target_hours-len(cooling_hours)]
            cooling_hours.extend([hour[0] for hour in hours_to_add])

        return sorted(cooling_hours)
