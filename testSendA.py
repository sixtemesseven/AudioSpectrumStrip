# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 23:48:58 2021

@author: justRandom
"""

import pyaudio
import numpy as np
from matplotlib import pyplot as plt
import scipy.fft as fft
import scipy.signal as sig
import numpy
import serial
import time
import wave

ser = serial.Serial('COM3', baudrate=115200, timeout=5)
sendFlag = False

def packAudioToBytestream(data):
    return data.tobytes()
    
chunksize = 1000
av = 5
amplification = 20
fadeFactor = 0.80
fftBinBuffer = numpy.zeros(int(chunksize / 2) + 1)

while(True):
    while ser.in_waiting:
        if(ser.read() == b'G'):
            if(ser.read() == b'\n'):
                sendFlag = True
                break
    
    if(sendFlag == True): 
        fftBinBuffer /= av 
        bin2send = fftBinBuffer[0:300]
        bin2send[10] = 255
        bin2send[11] = 25
        bin2send[12] = 5
        bin2send[13] = 1
        
        outArray = packAudioToBytestream(bin2send.astype(np.uint8)) + b'\xff'
        #print(len(outArray))
        #print(outArray)
        ser.write(outArray)
        fftBinBuffer *= fadeFactor
        sendFlag = False
