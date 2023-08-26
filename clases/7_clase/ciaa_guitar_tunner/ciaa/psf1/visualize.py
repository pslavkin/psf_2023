import numpy as np
import matplotlib.pyplot as plt
from   matplotlib.animation import FuncAnimation
import os
import io
import serial
import scipy.fftpack as sc
from   scipy.io.wavfile import write

STREAM_FILE=("/dev/ttyUSB3","serial")
#STREAM_FILE=("log.bin","file")
header = { "pre": b"*header*", "id": 0, "N": 128, "fs": 1000, "M":0,"convLength":0,"maxValue":0,"maxIndex":0,"maxPromIndex":0,"pos":b"end*" }

CHORD_WIDTH=2
chordsFrecs=[82.41 ,110.00 ,146.83 ,196.00 ,246.94 ,329.63]
chordsColors=["green","yellow","red","blue","magenta","black"]

fig    = plt.figure (3)
fig.suptitle("CIAA Guitar Tuner",fontsize=20)
adcAxe = fig.add_subplot ( 3,1,1 )
adcAxe.grid ( True )
adcLn, = plt.plot ( [0],[0],'b-o',label="adc",linewidth=10,alpha=0.2 )
adcAxe.set_xlim ( 0 ,(header["N"]-1))
adcAxe.set_ylim ( -0.6 ,0.6    )

ciaaDftAxe  = fig.add_subplot ( 3,1,3 )
ciaaDftAxe.grid ( True )
ciaaDftLn ,= plt.step ( [0] ,[0] ,'k-' ,label="ciaa-FFT"   ,linewidth=1 ,alpha=0.8 )
ciaaMaxLn ,= plt.plot ( 0   ,0   ,'bo' ,label="max"        ,linewidth=10 ,alpha=0.8)
ciaaFftLn ,= plt.plot ( 0   ,0   ,'m-' ,label="python-FFT" ,linewidth=10 ,alpha=0.2 )
ciaaDftAxe.set_xlim ( 0  ,header["fs"]//2   )
ciaaDftAxe.set_ylim ( 0 ,300)
ciaaLegendLn=ciaaDftAxe.legend(loc='upper right',prop={'size': 10})
for i in range(6):
    ciaaDftAxe.fill_between([chordsFrecs[i]-CHORD_WIDTH,chordsFrecs[i]+CHORD_WIDTH],-10,2000,facecolor = chordsColors[i],alpha=0.4)


chordLn=[]
for i in range(6):
    chordAxe          = fig.add_subplot ( 3,6,7+i )
#    chordAxe.fill_between( chordsFrecs[i]-CHORD_WIDTH,chordsFrecs[i]+CHORD_WIDTH,0,10,facecolor = "green",alpha   = 0.4)
    chordAxe.set_xlim ( chordsFrecs[i]-CHORD_WIDTH  ,chordsFrecs[i]+CHORD_WIDTH   )
    chordAxe.set_ylim ( 0  ,10   )
    plt.axvline(chordsFrecs[i])
    Ln,  = plt.plot ( 0,0,'k',label=chordsFrecs[i])
    chordAxe.legend(loc='upper right',prop={'size': 10})
    chordLn.append(Ln)
    chordAxe.grid ( True )


ciaaDft = [1]

def findHeader(f,h):
    data=bytearray(b'12345678')
    while data!=h["pre"]:
        data+=f.read(1)
        if len(data)>len(h["pre"]):
            del data[0]

    h["id"]           = readInt4File(f,4)
    h["N" ]           = readInt4File(f)
    h["fs"]           = readInt4File(f)
    h["M"]            = readInt4File(f)
    h["convLength"]   = readInt4File(f)
    h["maxValue"]     = readInt4File(f)/2**0
    h["maxIndex"]     = readInt4File(f,4)
    h["maxPromIndex"] = readInt4File(f)*header["fs"]/(header["convLength"]*20)

    data=bytearray(b'1234')
    while data!=h["pos"]:
        data+=f.read(1)
        if len(data)>len(h["pos"]):
            del data[0]
    print({k:round(v,2) if isinstance(v,float) else v for k,v in h.items()})
    return h["id"],h["N"],h["fs"],h["M"],h["convLength"],h["maxValue"],h["maxIndex"],h["maxPromIndex"]


def readInt4File(f,size=2,sign=False):
    raw=f.read(1)
    while( len(raw) < size):
        raw+=f.read(1)
    return (int.from_bytes(raw,"little",signed=sign))

def flushStream(f,h):
    if(STREAM_FILE[1]=="serial"): #pregunto si estoy usando la bibioteca pyserial o un file
        f.flushInput()
    else:
        f.seek ( 2*h["N"],io.SEEK_END)

def readFile(f):
    global header
    flushStream ( streamFile,header )
    id,N,fs,M,convLength,maxValue,maxIndex,maxPromIndex=findHeader ( streamFile,header )
    ciaaDft    = []
    adc        = []
    for chunk in range(N):
        adc.append     ( readInt4File(f,sign=True )/(2**15))
        ciaaDft.append ( readInt4File(f,sign=True ))
    for chunk in range(convLength-N):
        adc.append (0)
    return maxPromIndex,maxIndex,maxValue,adc,ciaaDft

def init():
    return adcLn,

def update(t):
    global dft,ciaaDft,fs,maxIndex,chordLn
    maxPromIndex,maxIndex,maxValue,adc,ciaaDft=readFile(streamFile)
    nData = np.arange(0,header["convLength"],1)
    time = nData/header["fs"]
    frec = np.linspace(0,header["fs"]//2,header["convLength"]//2)

    adcLn.set_data(nData,adc)
    ciaaFftLn.set_data(frec,np.abs(np.fft.fft(adc)[:header["convLength"]//2])**2)
    firstIndex=max(maxIndex-header["N"]//2,0)
    lastIndex=min(header["convLength"]//2,firstIndex+header["N"])
    ciaaDftLn.set_data(frec[firstIndex:lastIndex],ciaaDft[:lastIndex-firstIndex])
    ciaaMaxLn.set_data(frec[maxIndex],maxValue)
    ciaaMaxLn.set_label(round(maxPromIndex,2))
#
    multiIndex=np.full(10,maxPromIndex)
    multiData=np.arange(0,10,1)
    for i in chordLn:
        i.set_data(multiIndex,multiData)
        i.set_data(multiIndex,multiData)
        i.set_data(multiIndex,multiData)
        i.set_data(multiIndex,multiData)
        i.set_data(multiIndex,multiData)
        i.set_data(multiIndex,multiData)
    return adcLn,ciaaDftLn,ciaaMaxLn,chordLn[0],chordLn[1],chordLn[2],chordLn[3],chordLn[4],chordLn[5],ciaaFftLn

#seleccionar si usar la biblioteca pyserial o leer desde un archivo log.bin
if(STREAM_FILE[1]=="serial"):
    streamFile = serial.Serial(port=STREAM_FILE[0],baudrate=460800,timeout=None)
else:
    streamFile=open(STREAM_FILE[0],"rb",0)

ani=FuncAnimation(fig, update, 100000, init, blit=True, interval=10, repeat=True)
plt.get_current_fig_manager().window.showMaximized()
plt.show()
streamFile.close()

