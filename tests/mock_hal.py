class MockChargerHAL:
    def __init__(self):
        self.cp_voltage = 12.0
        self.current_limit = 0
        self.relay_state = False

    def set_current_limit(self, current_limit):
        self.current_limit = current_limit

    def relay_on(self):
        self.relay_state = True

    def relay_off(self):
        self.relay_state = False

    def initiate_cp_pin_high(self):
        self.cp_voltage = 12.0

    def cp_top_voltage(self):
        return self.cp_voltage

    def set_cp_voltage(self, voltage):
        self.cp_voltage = voltage
