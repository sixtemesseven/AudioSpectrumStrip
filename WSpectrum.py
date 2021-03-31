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

ser = serial.Serial('COM8', baudrate=115200, timeout=0)

# initialize portaudio
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print( "Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))           
chunksize = 4096

stream = p.open(format=pyaudio.paInt16, channels=1, input_device_index = 0, rate=48000, input=True, frames_per_buffer=chunksize)

def audioFFT(data):
        fftd = fft.rfft(data)     
        fftd = (abs(fftd)) #Scale to 0-255
        return fftd

def packAudioToBytestream(data):
    return data.tobytes()

def getAudio(chunksize):
    data = stream.read(chunksize)
    return np.frombuffer(data, dtype=np.int16)

   

amplification = 90
fadeFactor = 0.6
fftBinBuffer = numpy.zeros(int(chunksize / 2) + 1)
equalArray = numpy.linspace(1, 1.5, 300) 

while(True):
    
    audio = getAudio(chunksize)
    fftBinBuffer += audioFFT(amplification * audio)
    bin2send = numpy.zeros(300)
    buffer = 0
    for i in range (102):
        bin2send[i] = fftBinBuffer[buffer]
        buffer += 1
    for i in range (66):
        bin2send[102 + i] = (fftBinBuffer[buffer] + fftBinBuffer[buffer + 1])/2
        buffer += 2
    for i in range (66):
        bin2send[168 + i] = (fftBinBuffer[buffer] + fftBinBuffer[buffer + 1] + fftBinBuffer[buffer + 2] + fftBinBuffer[buffer + 3])/4
        buffer += 4
    for i in range (66):
        bin2send[234 + i] = (fftBinBuffer[buffer] + fftBinBuffer[buffer + 1] + fftBinBuffer[buffer + 2] + fftBinBuffer[buffer + 3] + fftBinBuffer[buffer + 4] + fftBinBuffer[buffer + 5])/6
        buffer += 6

    bin2send = numpy.clip(numpy.round(abs(bin2send / 65536)), 0, 254) * equalArray
    outArray = packAudioToBytestream(bin2send.astype(np.uint8)) + b'\xff'
    
    fftBinBuffer *= fadeFactor
    

    #Wait for request from ESP
    while(True):
        if(ser.in_waiting > 0):
            if(ser.read() == b'G'):
                if(ser.read() == b'\n'):
                    #Send the prepared array
                    ser.write(outArray)
                    break
                

