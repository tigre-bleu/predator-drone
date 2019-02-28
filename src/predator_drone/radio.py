#
# nRF24L01+ chip management
#

import RPi.GPIO as GPIO
from RF24 import *
import time

from . import disp


# ===============
#    Constants
# ===============

CONFIG_CE_PIN = RPI_V2_GPIO_P1_22
CONFIG_CS_PIN = RPI_V2_GPIO_P1_24


# ======================
#    nRF24L01 manager
# ======================

class RadioManager():
    def __init__(self):
        num_rf_channels = 4
        chans = [0] * num_rf_channels
        start_chans_1 = [0x0a, 0x1a, 0x2a, 0x3a]
        start_chans_2 = [0x2a, 0x0a, 0x42, 0x22]
        start_chans_3 = [0x1a, 0x3a, 0x12, 0x32]
        self.start_chans_list = [start_chans_1, start_chans_2, start_chans_3]

        disp.debug("Initializing radio module nRF24L01+")
        self.nrf = RF24(CONFIG_CE_PIN, CONFIG_CS_PIN, BCM2835_SPI_SPEED_8MHZ)
        self.nrf.begin()
        self.nrf.setChannel(1)
        self.nrf.setPALevel(RF24_PA_MAX)
        self.nrf.setAutoAck(False)
        self.nrf.setDataRate(RF24_250KBPS)
        disp.debug("Radio module initialized")


    def set_channel(self, channel):
        self.nrf.stopListening()
        time.sleep(0.01)
        self.nrf.setChannel(channel)
        self.nrf.startListening()
        disp.debug("RF24 channel set to", str(channel))


    def set_rx(self):
        self.nrf.setAddressWidth(2)
        self.nrf.payloadSize = 15
        self.nrf.disableCRC()
        self.nrf.openReadingPipe(1, 0xAA)
        disp.debug("RF24 set to RX mode")


    def set_tx(self, address):
        self.nrf.setAddressWidth(5)
        self.nrf.payloadSize = 10
        self.nrf.setCRCLength(RF24_CRC_16)
        self.nrf.openWritingPipe(address)
        disp.debug("RF24 set to TX mode (to address", address + ")")

