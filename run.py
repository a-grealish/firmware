from hal import ChargerHAL
from j1772 import J1772Charger

def main() -> None:
    hal = ChargerHAL()
    charger = J1772Charger(hal)
    charger.monitor_charging()

if __name__ == "__main__":
    main()
