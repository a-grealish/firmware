import argparse
import logging

from hal import ChargerHAL
from j1772 import J1772Charger

def main() -> None:
    hal = ChargerHAL()
    charger = J1772Charger(hal)
    charger.monitor_charging()


def setup_loggers(loglevel: str) -> None:
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', dest='log', type=str, help='Set the log level, DEBUG, INFO, ..')
    args = parser.parse_args()

    setup_loggers(args.log)

    main()
