import logging
from statistics import fmean
from time import sleep

from gpiozero import PWMOutputDevice, DigitalOutputDevice, SPIDevice, MCP3001

logger = logging.getLogger(__name__)

class ChargerHAL:
    def __init__(self):
        self.control_pilot = PWMOutputDevice(pin="GPIO12", frequency=1000)

        # Todo: Catch the warning for disabled SPI device
        self.energy_monitor = SPIDevice(port=0, device=0)

        self.cp_adc = MCP3001(port=0, device=1, max_voltage=5.0)

        self.relay = DigitalOutputDevice(
            pin="GPIO5",
            active_high=True,
            initial_value=False
        )

    def initiate_cp_pin_high(self):
        self.control_pilot.value = 1.0

    def _set_cp_pwm(self, pwm_value: float) -> None:
        self.control_pilot.value = pwm_value

    def set_current_limit(self, amps: int) -> None:
        # Todo: Move this logic into j1772 class
        if amps < 6:
            pwm_value = 0.0
        elif amps > 80:
            pwm_value = 1.0
        else:
            pwm_value = (amps - 6) / 24 * 0.4 + 0.1

        self._set_cp_pwm(pwm_value)

    def read_cp_voltage(self) -> float:
        # Voltage adjusts for the max_voltage reference of 5V
        # Multiply by the power board scaling factor to get the true top
        # value of the CP Pin. This was measured at 6.3x
        return self.cp_adc.voltage * 6.3

    def cp_top_voltage(self):
        voltages = []

        # This is designed to sample over a full PWM cycle at 1 khz, but I've assumed
        # that reading the ADC and appending to a list has no impact of the time. This
        # is probably true, but we could check.
        for i in range(1000):
            v = self.read_cp_voltage()
            voltages.append(v)
            sleep(0.00001)

        cp_voltage_max = max(voltages)
        cp_voltage_min = min(voltages)

        # If we're in a PWM mode, only average the "high" voltages
        if cp_voltage_min > 3:
            logger.debug("A PWM output was detected, averaging just the high values")
            mid_point = (cp_voltage_max + cp_voltage_min) / 2
            cp_voltage_top = fmean([v for v in voltages if v > mid_point])
        else:
            cp_voltage_top = fmean(voltages)

        logger.info(f"CP Top Voltage Read as: {cp_voltage_top}")
        logger.debug(voltages)

        return cp_voltage_top

    def read_ac_voltage(self) -> float:
        # Implement the logic to read voltage from the SPI device
        # Return the voltage value
        pass

    def read_ac_current(self) -> float:
        # Implement the logic to read current from the SPI device
        # Return the current value
        pass

    def relay_on(self) -> None:
        self.relay.on()

    def relay_off(self) -> None:
        self.relay.off()
