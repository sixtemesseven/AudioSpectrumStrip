# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 11:43:41 2021

@author: justrandom
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
import socket

UDP_IP = "192.168.0.134"
UDP_PORT = 3333


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.bind((UDP_IP, UDP_PORT))

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print( "Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))           

chunksize = 4096
stream = p.open(format=pyaudio.paInt16, channels=1, input_device_index = 1, rate=48000, input=True, frames_per_buffer=chunksize)
amplification = 1
fadeFactor = 0.7
fftBinBuffer = numpy.zeros(int(chunksize / 2) + 1)
equalArray = numpy.linspace(1, 1.3, 300) 

def audioFFT(data):
        fftd = fft.rfft(data)     
        fftd = (abs(fftd)) #Scale to 0-255
        return fftd

def packAudioToBytestream(data):
    return data.tobytes()

def getAudio(chunksize):
    data = stream.read(chunksize)
    return np.frombuffer(data, dtype=np.int16)

audio = np.zeros(chunksize)

while True:
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
        
    obuf = numpy.round(abs(bin2send / 90)) * equalArray
    bin2send = np.zeros(900)
    i = 0 
    
    
    for z in range(len(obuf)):
        if(obuf[z] < 255):
            #Green Channel
            bin2send[i+1] = obuf[z]
            bin2send[i+2] = 0
            i +=3
        elif(obuf[z] <= (255 + 240)):
            #Yellow Channel
            bin2send[i] = obuf[z] - 240
            bin2send[i+1] = obuf[z] - 240
            i +=3
        else:
            #Red Channel
            bin2send[i] = obuf[z] - 490
            i +=3  
            
    numpy.clip(bin2send, 0, 255)
    outArray = packAudioToBytestream(bin2send.astype(np.uint8))
    
    fftBinBuffer *= fadeFactor
    
    while(True):    
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        if(data == b'Send Data\n'):
            sock.sendto(outArray, addr)
            break;
    



