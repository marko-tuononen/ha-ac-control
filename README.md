# ha-ac-control
Home Assistant integration for dynamically controlling air conditioning based on real-time electricity prices from Nordpool.

## Setup
Functionality has been implemented using a combination of Home Assistant's automation features and its Python Scripts integration. Please follow the steps below to set up the full solution:

1. **Clone Repository**: Clone this repository to the `python_scripts` directory under your Home Assistant's configuration directory.

    ```sh
    git clone https://github.com/marko-tuononen/ha-ac-control /path/to/homeassistant/config/python_scripts
    ```

2. **Define Input Booleans**: In your `configuration.yaml`, define input booleans for each hour to represent whether the AC should run during that hour tomorrow. Separate sets for today (`cooling_hour_0` to `cooling_hour_23`) and tomorrow (`cooling_hour_tomorrow_0` to `cooling_hour_tomorrow_23`). See example from `examples/configuration.yaml`.

3. **Create Automations**: Create automations in your `automations.yaml` file. See example from `examples/automation.yaml`.

   - **Run the Python Script (cooling_hours.py)**: Create an automation that runs the Python script at 6 PM every day to prepare the schedule for the next day. The Python script calculates the cooling hours for the next day and updates the corresponding input booleans.

   - **Transfer Booleans at Midnight**: Create an automation that transfers the input booleans from the next day to the current day at midnight.

   - **Control the AC**: Create an automation that checks the input booleans each hour to decide whether to turn the AC on or off.

This setup ensures that your automation follows the correct input booleans for the appropriate day, allowing for more accurate and timely control of your AC based on electricity prices.

Note! The following dependencies have been used in the examples.
- [Nord Pool integration for Home Assistant](https://github.com/custom-components/nordpool)
- [Toshiba AC integration for Home Assistant](https://github.com/h4de5/home-assistant-toshiba_ac)

## Run Unit Tests
You can run unit tests to ensure the functionality of the Python Script (cooling.hours.py):

```sh
python -m unittest
