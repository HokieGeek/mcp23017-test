#!/usr/bin/python

from pyBusPirateLite.I2C import *
import sys
import signal, os
import time

device_address=0x40
values=[0b10000001, 0b01000010, 0b00100100, 0b00011000]

i2c = I2C("/dev/ttyUSB0", 115200, 5)
i2c.BBmode()
i2c.enter_I2C()
i2c.cfg_pins(I2CPins.POWER | I2CPins.PULLUPS)
i2c.set_speed(I2CSpeed._400KHZ)

def setVal(address, val):
    i2c.send_start_bit()
    i2c.bulk_trans(3, [device_address, address, val])
    i2c.send_stop_bit()

def setPinsOut(val):
    setVal(0x12, val) # ... [MAGIC NUMBER] why this value as the address?

def intHandler(signum, frame):
    print "Exiting..."
    i2c.resetBP()
    sys.exit()

#def setPinsOutArray(array, delay=1):
    #for val in array:
        #time.sleep(delay);
        #setPinsOut(val)

signal.signal(signal.SIGINT, intHandler)

setVal(0, 0)
while True:
    #setPinsOutArray(values[:-1])
    #setPinsOutArray(values[1:])
    for val in values[:-1]:
        time.sleep(1);
        setPinsOut(val)
    for val in reversed(values[1:]):
        time.sleep(1);
        setPinsOut(val)
