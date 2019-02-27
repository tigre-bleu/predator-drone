#
# Syma X5C-1 drone scanner
#

import time

from .radio import Radio
from . import disp


# ========================
#    Syma scanner class
# ========================

class SymaScanner():

    def __init__(self):
        self.drones = {}
        self.seen_drones = {}

        disp.debug("Initializing radio")
        self.radio = Radio()
        self.radio.set_rx()


    # =========================
    #    Searching for drone
    # =========================

    def scan(self):
        self.scan_radio()
        self.identify_drones()
        return self.drones


    def scan_radio(self):
        disp.info("Searching for Syma X5C-1")

        for start_chans in self.radio.start_chans_list:
            disp.debug("Searching in channels", str(start_chans))

            # Scan the channels known to be Syma XC-1  4 by 4
            for channel in start_chans:
                self.radio.set_channel(channel)

                time.sleep(0.1)

                for i in range(10):
                    time.sleep(0.02)
                    while self.radio.nrf.available():
                        data = self.radio.nrf.read(self.radio.nrf.payloadSize)
                        computed_crc = int(
                                data[5] ^ data[6] ^ data[7] ^ data[8] ^ data[9]
                                ^ data[10] ^ data[11] ^ data[12] ^ data[13]     ) + 0x55
                        received_crc = data[14]
                        hex_data = str(data).encode('hex')

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
                            if not target_address in self.drones.keys():
                                self.drones[target_address] = {}

                            # Add channel to seen list
                            if not channel in self.drones[target_address].keys():
                                self.drones[target_address][channel] = True


    def identify_drones(self):
        consolidated_drones = {}
        for start_chans in self.radio.start_chans_list:
            # Check if a valid frame has been found on each of the expected 4 channels
            for address in self.drones:
                drone = self.drones[address]
                i=0
                for channel in start_chans:
                    if channel in drone.keys():
                        i = i+1
                if (i==4):
                    consolidated_drones[address]=drone.keys()

        # Clean self.drones to keep only the ones that are valid on 4 channels
        self.drones = consolidated_drones



    # ==================
    #    Print drones
    # ==================

    def display_drones(self):
        if not self.drones:
            disp.info("No drone found")

        for address in self.drones:
            drone = self.drones[address]
            disp.item1("Syma X5C-1 Drone found with address", address, "on channels",
                    '[%s]' % ', '.join(map(str, drone)) )

