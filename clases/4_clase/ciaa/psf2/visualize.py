#!python3
import numpy as np
import matplotlib.pyplot as plt
from   matplotlib.animation import FuncAnimation
import struct
import os
import io
import serial

STREAM_FILE=("/dev/ttyUSB3","serial")
#STREAM_FILE=("log.bin","file")

header = { "head": b"head", "id": 0, "N": 64, "fs": 10000,"tail":b"tail" }
fig    = plt.figure ( 1 )

adcAxe = fig.add_subplot ( 2,1,1                  )
adcLn, = plt.plot        ( [],[],'r-',linewidth=4 )
adcAxe.grid              ( True                   )
adcAxe.set_ylim          ( -1.65 ,1.65            )

corrAxe      = fig.add_subplot ( 2,1,2                               )
corrLn,      = plt.plot        ( [],[],'b-',linewidth = 5,alpha = 1 )
thresholdLn, = corrAxe.plot([],[],'r-',linewidth      = 2,alpha = 0.8)
corrAxe.grid ( True )

def findHeader(f,h):
    find=False
    while(not find):
        data=bytearray(len(h["head"]))
        while data!=h["head"]:
            data+=f.read(1)
            data[:]=data[-4:]

        h["id"]       = readInt4File(f,4)
        h["N" ]       = readInt4File(f)
        h["fs"]       = readInt4File(f)

        data=bytearray(b'1234')
        for i in range(4):
            data+=f.read(1)
            data[:]=data[-4:]
        find = data==h["tail"]

    print({k:round(v,2) if isinstance(v,float) else v for k,v in h.items()})
    return h["id"],h["N"],h["fs"]

def readInt4File(f,size=2,sign=False):
    raw=f.read(1)
    while( len(raw) < size):
        raw+=f.read(1)
    return (int.from_bytes(raw,"little",signed=sign))

def readFloat4File(f,size=4):
    raw=f.read(1)
    while( len(raw) < size):
        raw+=f.read(1)
    return struct.unpack('<f',raw)[0]

def flushStream(f,h):
    if(STREAM_FILE[1]=="serial"): #pregunto si estoy usando la bibioteca pyserial o un file
        f.flushInput()
    else:
        f.seek ( 2*h["N"],io.SEEK_END)

def readSamples(adc,corr,N):
    for i in range(N):
        adc[i]      = readFloat4File(streamFile)*1.65
        corr[2*i]   = readFloat4File(streamFile)
        corr[2*i+1] = readFloat4File(streamFile)

stop=False

def update(t):
    global header,stop
#    flushStream ( streamFile,header )
    if stop:
        input()
        stop=False

    id,N,fs=findHeader ( streamFile,header )
    adc      = np.zeros(N).astype(float)
    ciaaCorr = np.zeros(2*N).astype(float)
    timeN    = np.arange(0,2*N-1,1)
    readSamples(adc,ciaaCorr,N)

    adcAxe.set_xlim ( 0          ,(2*N-1)/fs )
    adcLn.set_data  ( timeN[0:N]/fs ,adc   )

    corrLn.set_data ( timeN ,ciaaCorr[:2*N-1])
    corrAxe.set_ylim ( 0 ,1.65)
    corrAxe.set_xlim ( 0 ,2*N-1)
    THR=1.0
    thresholdLn.set_data(timeN,np.ones(2*N-1)*THR)

    m=max(ciaaCorr[:N-1])
    if m>THR and m<10:
        print("find",m,np.where(m==ciaaCorr)[0])
        stop=True


    return adcLn, corrLn,   thresholdLn,

#seleccionar si usar la biblioteca pyserial o leer desde un archivo log.bin
if(STREAM_FILE[1]=="serial"):
    streamFile = serial.Serial(port=STREAM_FILE[0],baudrate=460800,timeout=None)
else:
    streamFile=open(STREAM_FILE[0],"rb",0)

ani=FuncAnimation(fig,update,10000,init_func=None,blit=True,interval=10,repeat=True)
plt.draw()
plt.get_current_fig_manager().window.showMaximized() #para QT5
plt.show()
streamFile.close()
