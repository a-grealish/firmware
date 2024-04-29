from gpiozero import PWMOutputDevice, DigitalOutputDevice, InputDevice, SPIDevice


class ChargerHAL:
    def __init__(self):
        self.control_pilot = PWMOutputDevice(pin="GPIO12", frequency=1000)

        # Todo: Check this pull-up
        self.control_pilot_read = InputDevice(pin="GPIO3", pull_up=True)

        # Todo: Catch the warning for disabled SPI device
        self.energy_monitor = SPIDevice(port=0, device=0)

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
        return self.control_pilot_read.value * 3.3

    def read_voltage(self) -> float:
        # Implement the logic to read voltage from the SPI device
        # Return the voltage value
        pass

    def read_current(self) -> float:
        # Implement the logic to read current from the SPI device
        # Return the current value
        pass

    def relay_on(self) -> None:
        self.relay.on()

    def relay_off(self) -> None:
        self.relay.off()
