from enum import Enum
import time
from hal import ChargerHAL

MAX_CURRENT = 6


class CPState(Enum):
    VEHICLE_NOT_CONNECTED = "Vehicle not connected"
    VEHICLE_CONNECTED_NOT_READY = "Vehicle connected, not ready to charge"
    VEHICLE_CONNECTED_READY = "Vehicle connected, ready to charge"
    VEHICLE_CHARGING = "Vehicle charging"
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
        print("Charging stopped")

    def get_charging_status(self) -> None:
        if self.is_charging:
            voltage = self.hal.read_voltage()
            current = self.hal.read_current()
            power = voltage * current
            print(
                f"Charging status: {self.charging_current}A, {voltage}V, {current}A, {power}W")
        else:
            print("Not charging")

    def read_cp_state(self) -> CPState:
        cp_voltage = self.hal.read_cp_voltage()

        if 0.0 <= cp_voltage < 3.0:
            return CPState.VEHICLE_NOT_CONNECTED
        elif 3.0 <= cp_voltage < 8.0:
            return CPState.VEHICLE_CONNECTED_NOT_READY
        elif 8.0 <= cp_voltage < 11.0:
            return CPState.VEHICLE_CONNECTED_READY
        elif 11.0 <= cp_voltage < 12.0:
            return CPState.VEHICLE_CHARGING
        else:
            return CPState.UNKNOWN

    def monitor_charging(self) -> None:
        # Set a 12V signal initially
        self.hal.initiate_cp_pin_high()

        while True:
            cp_state = self.read_cp_state()
            print("CP State:", cp_state.value)

            if cp_state == CPState.VEHICLE_CONNECTED_READY and not self.is_charging:
                self.start_charging(MAX_CURRENT)
            elif cp_state == CPState.VEHICLE_NOT_CONNECTED and self.is_charging:
                self.stop_charging()

            if self.is_charging:
                self.get_charging_status()

            time.sleep(1)  # Delay between CP state checks
