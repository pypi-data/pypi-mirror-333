#!/usr/bin/env python3

import argparse

from p3lib.uio import UIO
from p3lib.helper import logTraceBack

# PJA REMOVE, FOR TEST PURPOSES only
import random


class CM2100B(object):
    """@brief Responsible for an interface to the OWON CM2100B current clamp meter."""

    def __init__(self, mac, uio=None):
        """@brief Constructor.
           @param The bluetooth MAC address of the CM2100B current clamp meter.
           @param uio A UIO instance or None. If a UIO instance is passed then debug messages
                  may be displayed when the _debug(msg) method is called."""
        self._mac = mac
        self._uio = uio

    # PJA TODO
    def get_amps(self):
        """@brief Get the amps measured by the meter."""
        r = random.randint(-40, 40)
        r = r/100.0
        return 8.0 + r

    def disconnect(self):
        pass


def main():
    """@brief Program entry point"""
    uio = UIO()

    try:
        parser = argparse.ArgumentParser(description="An interface to the CM2100B current clamp DMM.",
                                         formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument(
            "-d", "--debug",   action='store_true', help="Enable debugging.")
        parser.add_argument(
            "-m", "--mac",     help="The bluetooth MAC address of the CM2100B meter.", default=None, required=True)

        options = parser.parse_args()

        uio.enableDebug(options.debug)

    # If the program throws a system exit exception
    except SystemExit:
        pass
    # Don't print error information if CTRL C pressed
    except KeyboardInterrupt:
        pass
    except Exception as ex:
        logTraceBack(uio)

        if options.debug:
            raise
        else:
            uio.error(str(ex))


if __name__ == '__main__':
    main()
