# Script's internal parameters
THRESHOLD_0 = 2.822
THRESHOLD_1 = 5.644
TARGET_COOLING_HOURS = 12
COOLING_WEEKS = list(range(18,40))
FALLBACK_COOLING_HOURS = list(range(0,6)) + list(range(12,18))


def get_cooling_hours(current_week, prices_per_hour, price_thresholds, num_target_hours, cooling_weeks):
    if current_week not in cooling_weeks:
        return []
    
    cooling_hours = find_indices(
        prices_per_hour,
        lambda elem: elem <= price_thresholds[0]
    )
    if len(cooling_hours) < num_target_hours:
        candidate_hours = find_indices(
            prices_per_hour,
            lambda elem: elem > price_thresholds[0] and elem <= price_thresholds[1]
        )
        hours_to_add = sorted(
            [(hour, prices_per_hour[hour]) for hour in candidate_hours],
            key=lambda elem: elem[1]
        )[:num_target_hours-len(cooling_hours)]
        cooling_hours.extend([hour[0] for hour in hours_to_add])

    return sorted(cooling_hours)


def find_indices(lst, condition):
    return [idx for idx, elem in enumerate(lst) if condition(elem)]

try:
    # Fetch the necessary parameters
    iso_date = hass.states.get('sensor.date_time_iso').state
    current_week = datetime.datetime.fromisoformat(iso_date).isocalendar()[1]
    prices_per_hour = hass.states.get('sensor.nordpool').attributes['tomorrow']

    # Find actual cooling hours
    cooling_hours = []
    if prices_per_hour is not None and len(prices_per_hour) == 24:
        cooling_hours = get_cooling_hours(
            current_week,
            prices_per_hour,
            [THRESHOLD_0, THRESHOLD_1],
            TARGET_COOLING_HOURS,
            COOLING_WEEKS
        )
        logger.info("Cooling hours calculated successfully.")
    else:
        cooling_hours = FALLBACK_COOLING_HOURS
        logger.warning("Unable to read tomorrow's electricity prices from Nordpool sensor, using fallback cooling hours.")

    logger.info(f"Cooling hours for tomorrow: {cooling_hours}")

    # Store the result in input_booleans for each hour of tomorrow
    for hour in range(24):
        input_boolean_entity = f"input_boolean.cooling_hour_tomorrow_{hour}"
        if hour in cooling_hours:
            hass.services.call('input_boolean', 'turn_on', {'entity_id': input_boolean_entity})
        else:
            hass.services.call('input_boolean', 'turn_off', {'entity_id': input_boolean_entity})

except NameError:
    pass  # to enable unit testing

except Exception as e:
    logger.error(f"Exception occurred: {e}")
