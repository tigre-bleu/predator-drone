#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import threading
import time
import operator

from RF24 import *
import RPi.GPIO as GPIO

import select
import tty
import termios

import re
import csv

from collections import defaultdict
import itertools

stat = {}

log_file_raw = open("nrf24_raw.log", "w")
log_file_filtered = open("nrf24_filtered.log", "w")

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def setup(channel, address, data_rate, crc = 0):
    global initial_clock, last_clock, frame_seq
    if not crc:
        radio.disableCRC()
    else:
        radio.setCRCLength(crc)
    radio.stopListening()
    radio.payloadSize =payload_size
    time.sleep(0.01)
    radio.setDataRate(data_rate)
    radio.setChannel(channel)
 
    radio.openReadingPipe(1, address)
    radio.startListening()

    frame_seq = 0
    log_file_raw.write("id,time,channel,data,delta\n")
    print("Press 'q' to finish")

def log(channel, data):
    global initial_clock, last_clock, frame_seq
    if frame_seq == 0:
        initial_clock=time.clock()
        last_clock=initial_clock
    frame_seq = frame_seq + 1
    current_clock = time.clock()
    delta_clock = current_clock - last_clock
    log_file_raw.write(str(frame_seq)+","+str(current_clock)+","+str(channel)+","+data+","+str(delta_clock)+"\n")
    #print(str(frame_seq)+";"+str(current_clock)+";"+str(channel)+";"+data+";"+str(delta_clock)+"\n")
    last_clock = current_clock

old_settings = termios.tcgetattr(sys.stdin)

address = 0xAAA1CA201670
data_rate = RF24_250KBPS
payload_size = 10
channel = 10
aack = False

radio = RF24(RPI_V2_GPIO_P1_22, RPI_V2_GPIO_P1_24, BCM2835_SPI_SPEED_8MHZ)
radio.begin()
radio.setChannel(channel)
radio.setPALevel(RF24_PA_MAX)
radio.setAutoAck(aack)
radio.setDataRate(RF24_250KBPS)
radio.setAddressWidth(2)
radio.disableCRC()
radio.payloadSize = payload_size

setup(channel, address, data_rate)
try:
    tty.setcbreak(sys.stdin.fileno())
    running = True
    while (running):
        if isData():
            if (1):
                c = sys.stdin.read(1)
                if c == '\x1b' or c == 'q' or c == 'Q':
                    running = False
                    break

        while(radio.available()):
            data = radio.read(payload_size)
            hex_data = str(data).encode('hex')
            log(channel, hex_data)
    print "Ending"
    log_file_raw.close()

    # Filtering correct packets

    # Fill lists from raw log
    columns = defaultdict(list)
    with open("nrf24_raw.log") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for (k,v) in row.items():
                columns[k].append(v)

    # Filter only valid frames
    log_file_raw.close()
    with open("nrf24_raw.log") as f:
        reader = csv.DictReader(f)
        i=0
        last_clock = 0
        log_file_filtered.write("id,time,channel,data,delta\n")
        first_line = True
        for row in reader:
            i = i+1
            data=[]
            data.append(row['data'][0:2])
            data.append(row['data'][2:3])
            data.append(row['data'][4:6])
            data.append(row['data'][6:8])
            data.append(row['data'][8:10])
            data.append(row['data'][10:12])
            data.append(row['data'][12:14])
            data.append(row['data'][14:16])
            data.append(row['data'][16:18])
            data.append(row['data'][18:20])
            data=[int(x, 16) for x in data]
            received_crc = int(data[9])
            computed_crc = int(data[0] ^ data[1] ^ data[2] ^ data[3] ^ data[4] ^ data[5] ^ data[6] ^ data[7] ^ data[8]) + 0x55
            if received_crc == computed_crc:
                if first_line:
                    first_line = False
                    last_clock = float(row['time'])
                else:
                    current_clock = float(row['time'])
                    delta_clock = current_clock - last_clock
                    log_file_filtered.write(str(i)+","+str(current_clock)+","+row['channel']+","+row['data']+","+str(delta_clock)+"\n")
                    last_clock = current_clock
    log_file_filtered.close()

    # Compute statistics from filtered file
    columns = defaultdict(list)
    with open("nrf24_filtered.log") as f:
        reader = csv.DictReader(f)
        first_line = True
        first_time = 0
        # Removing first line as the delta is not correct
        for row in reader:
            if first_line:
                first_line = False
            else:
                for (k,v) in row.items():
                    if k=='delta':
                        columns[k].append(float(v))
                    else:
                        columns[k].append(v)

    mean_delta = sum(columns['delta'])/len(columns['delta'])
    print "Mean value between valid frames: "+str(mean_delta)+"s"

finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
