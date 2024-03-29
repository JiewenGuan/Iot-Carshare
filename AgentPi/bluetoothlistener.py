"""
This module performs the functions associated with the
bluetooth recognition of users. It serves this function
by periodically or (relatively) instantaneously collecting the MAC addresses 
of active devices that are in range of the Agent
device, comparing this to a previously collected set
of devices in the case of periodic testing, and then polls the master pi for any valid
engineer appointment for the vehicle ID.
"""

import bluetooth
import time

# To consolidate logs into one location.
import logging
log = logging.getLogger(__name__)

class BluetoothListenerEngineer():
    """
    This class encapsulates the functions required to 
    listen for bluetooth devices. It is instantiated
    with no parameters.
    Its primary functions :func:`listen_bluetooth` (accepts 
    one paramater as an int which is the interval 
    time in seconds between listen events) and 
    catch_bluetooth (no defined time) return a set of 
    devices that have persisted for at least the 
    defined time. The logic underpinning this is that 
    many devices will move within proximity but less 
    will persist - those that persist may be an engineer.
    For this to return, the device must be discoverable.
    """

    def __init__(self):
        pass

    def listen_bluetooth(self, listen_interval) -> list:
        """
        Called to return a set of persisting bluetooth 
        MAC addresses based on the :attr:`listen_interval` parameter.
        """

        # Listen for initial devices, then pause and listen
        # for final devices.
        initial_devices = bluetooth.discover_devices()
        log.info("Initial devices: {}".format(initial_devices))
        time.sleep(listen_interval)
        final_devices = bluetooth.discover_devices()
        log.info("Final devices: {}".format(final_devices))

        # Compare the lists and return a list of persisting
        # devices. Using list comprehension in case order
        # becomes significant in a future implementation.
        # persisting_devices = set(initial_devices).intersection(final_devices)
        # Pythonic but not very efficient (O(n^2) vs set comparison O(n)). This is okay
        # as we don't expect there to be many bluetooth devices that persist.
        persisting_devices = [x for x in initial_devices if x in final_devices]
        log.info("Persisting devices: {}".format(persisting_devices))
        return persisting_devices

    def catch_bluetooth(self) -> list:
        """
        Called to return a set of bluetooth MAC addresses
        that were detetected during the predetermined 
        detection period.
        """

        found_devices = bluetooth.discover_devices()
        log.info("Detected devices: {}".format(found_devices))
        return found_devices


if __name__ == "__main__":
    # For testing purposes.

    bttest = BluetoothListenerEngineer(10)
    persistingaddresses = bttest.listen_bluetooth()
    print("Persisting Addresses: {}".format(persistingaddresses))