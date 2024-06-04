import pytest

from j1772 import J1772Charger, CPState, MAX_CURRENT
from mock_hal import MockChargerHAL

@pytest.fixture
def virtual_charger():
    hal = MockChargerHAL()
    # TODO: Fix this with ABC HAL
    charger = J1772Charger(hal)
    return charger


def test_state_transitions():
    '''
    Test that the CP voltage is read correctly, and moves between states as expected
    '''

    # Test initial state
    assert virtual_charger.read_cp_state() == CPState.VEHICLE_NOT_CONNECTED

    # Test transition from State A to State B
    virtual_charger.hal.set_cp_voltage(9.0)
    assert virtual_charger.read_cp_state() == CPState.VEHICLE_CONNECTED

    # Test transition from State B to State C
    virtual_charger.hal.set_cp_voltage(6.0)
    assert virtual_charger.read_cp_state() == CPState.VEHICLE_CHARGING

    # Test transition from State C to State D
    virtual_charger.hal.set_cp_voltage(3.0)
    assert virtual_charger.read_cp_state() == CPState.VEHICLE_CHARGING_VENTILATION

    # Test transition from State D to State C
    virtual_charger.hal.set_cp_voltage(6.0)
    assert virtual_charger.read_cp_state() == CPState.VEHICLE_CHARGING

    # Test transition from State C to State B
    virtual_charger.hal.set_cp_voltage(9.0)
    assert virtual_charger.read_cp_state() == CPState.VEHICLE_CONNECTED

    # Test transition from State B to State A
    virtual_charger.hal.set_cp_voltage(12.0)
    assert virtual_charger.read_cp_state() == CPState.VEHICLE_NOT_CONNECTED

    # Test unknown state
    virtual_charger.hal.set_cp_voltage(4.0)
    assert virtual_charger.read_cp_state() == CPState.UNKNOWN


def test_relay_states():
    pass