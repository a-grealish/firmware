from enum import Enum
import time
from hal import ChargerHAL

MAX_CURRENT = 32


class CPState(Enum):
    VEHICLE_NOT_CONNECTED = "Vehicle not connected"
    VEHICLE_CONNECTED = "Vehicle connected, ready to charge"
    VEHICLE_CHARGING = "Vehicle charging"
    VEHICLE_CHARGING_VENTILATION = "Vehicle charging with ventilation"
    UNKNOWN = "Unknown state"


class J1772Charger:
    def __init__(self, hal: ChargerHAL):
        self.hal = hal
        self.charging_current = 0
        self.is_charging = False

    def start_charging(self, current_limit: int) -> None:
        self.charging_current = current_limit
        self.hal.set_current_limit(current_limit)
        self.hal.relay_on()
        self.is_charging = True
        print(f"Charging started with current limit: {current_limit}A")

    def stop_charging(self) -> None:
        self.hal.relay_off()
        self.is_charging = False
        self.charging_current = 0
        self.hal.initiate_cp_pin_high()
        print("Charging stopped")

    def get_charging_status(self) -> None:
        if self.is_charging:
            # TODO
            # voltage = self.hal.read_ac_voltage()
            # current = self.hal.read_ac_current()
            # power = voltage * current
            voltage = current = power = "--TODO--"
            print(
                f"Charging status: {self.charging_current}A, {voltage}V, {current}A, {power}W")
        else:
            print("Not charging")

    def read_cp_state(self) -> CPState:
        cp_voltage = self.hal.cp_top_voltage()

        if 11.4 <= cp_voltage <= 12.6:
            return CPState.VEHICLE_NOT_CONNECTED
        elif 8.36 <= cp_voltage <= 9.84:
            return CPState.VEHICLE_CONNECTED
        elif 5.48 <= cp_voltage <= 6.49:
            return CPState.VEHICLE_CHARGING
        elif 2.62 <= cp_voltage <= 3.25:
            return CPState.VEHICLE_CHARGING_VENTILATION
        else:
            return CPState.UNKNOWN

    def monitor_charging(self) -> None:
        # Set a 12V signal initially
        self.hal.initiate_cp_pin_high()

        while True:
            cp_state = self.read_cp_state()
            print("CP State:", cp_state.value)

            if cp_state == CPState.UNKNOWN:
                print("Unknown State - Stop Charging")
                self.stop_charging()

            if cp_state == CPState.VEHICLE_CONNECTED and not self.is_charging:
                print(f"Starting to charge at {MAX_CURRENT}A")
                self.start_charging(MAX_CURRENT)
            elif cp_state == CPState.VEHICLE_NOT_CONNECTED and self.is_charging:
                print("Stopping charging")
                self.stop_charging()

            if self.is_charging:
                self.get_charging_status()

            time.sleep(1)  # Delay between CP state checks
