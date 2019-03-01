#
# Syma X5C-1 drone scanner
#

import binascii
import time

from .syma_hack import SymaController
from .radio import RadioManager
from . import disp


# ========================
#    Syma scanner class
# ========================

class SymaScanner():

    def __init__(self, radio):
        # Init drones lists
        self.seen_drones         = {}       # Seen drones on different channels
        self.consolidated_drones = {}       # Only real drones (on the 4 expected channels)
        self.syma_hackers        = []       # List of hacking objects

        # Register radio module
        self.radio = radio



    # =========================
    #    Searching for drone
    # =========================

    def scan(self, menu):
        self.__scan_radio()
        self.__identify_drones()
        self.__register_drones()


    def __scan_radio(self):
        disp.info("Searching for Syma X5C-1")
        self.seen_drones = {}

        self.radio.set_rx()

        for start_chans in self.radio.start_chans_list:
            disp.debug("Searching in channels", str(start_chans))

            # Scan the channels known to be Syma XC-1  4 by 4
            for channel in start_chans:
                self.radio.set_channel(channel)

                time.sleep(0.1)

                for i in range(50):
                    time.sleep(0.02)
                    while self.radio.nrf.available():
                        data = self.radio.nrf.read(self.radio.nrf.payloadSize)
                        computed_crc = int(
                                data[5] ^ data[6] ^ data[7] ^ data[8] ^ data[9]
                                ^ data[10] ^ data[11] ^ data[12] ^ data[13]     ) + 0x55
                        received_crc = data[14]
                        hex_data = binascii.hexlify(data).decode()

                        if received_crc == computed_crc:
                            target_address = '0x{:02x}'.format(data[0]) \
                                    + '{:02x}'.format(data[1]) \
                                    + '{:02x}'.format(data[2]) \
                                    + '{:02x}'.format(data[3]) \
                                    + '{:02x}'.format(data[4])

                            disp.debug("Valid frame received on channel",
                                    str(channel), "with address",
                                    target_address, "(" + hex_data + ")")

                            # Add drone to seen list
                            if not target_address in self.seen_drones.keys():
                                self.seen_drones[target_address] = {}

                            # Add channel to seen list
                            if not channel in self.seen_drones[target_address].keys():
                                self.seen_drones[target_address][channel] = True


    def __identify_drones(self):
        self.consolidated_drones = {}

        for start_chans in self.radio.start_chans_list:
            # Check if a valid frame has been found on each of the expected 4 channels
            for address in self.seen_drones:
                drone = self.seen_drones[address]
                i=0
                for channel in start_chans:
                    if channel in drone.keys():
                        i = i+1
                if (i==4):
                    self.consolidated_drones[address]=drone.keys()


    def __register_drones(self):
        for address, channels in self.consolidated_drones.items():
            hacker = SymaController(self.radio, address, channels)

            if hacker not in self.syma_hackers:
                self.syma_hackers.append(hacker)
                menu.add_numbered_opt( ("Hack", str(hacker)), hacker.start )
                disp.item1("New Syma X5C-1 drone found with address", address)



    # ===================
    #    Listing stuff
    # ===================

    def show_detected_drones(self):
        print("Syma X5C-1 drones found:")

        if len(self.syma_hackers) == 0:
            disp.item0(disp.str_red("No drone found"))

        for hacker in self.syma_hackers:
            disp.item0(hacker)


    def clear_lists(self):
        self.syma_hackers = []
        disp.info("Syma X5C-1 list cleared")

