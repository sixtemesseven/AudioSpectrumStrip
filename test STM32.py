# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 23:48:58 2021

@author: justRandom
"""

import numpy as np
from matplotlib import pyplot as plt
import serial
import time


ser = serial.Serial('COM6', baudrate=115200, timeout=0)
for i in range(10):
    ser.write(b'\xff\x00\x03\x00\x00\x44\x11')
    time.sleep(0.250)
    print(ser.read())

ser.close()



