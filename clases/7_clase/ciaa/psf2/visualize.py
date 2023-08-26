#!python3
import numpy as np
import matplotlib.pyplot as plt
from   matplotlib.animation import FuncAnimation
import os
import io
import serial

STREAM_FILE=("/dev/ttyUSB3","serial")
#STREAM_FILE=("log.bin","file")

header = { "pre": b"*header*", "id": 0, "N": 100, "fs": 1000, "pos":b"end*" }
fig    = plt.figure ( 1 )
fig.suptitle('Antialias digital + downsampling con CIAA', fontsize=16)

#--------------------------ADC--------------------------
adcAxe = fig.add_subplot ( 2,1,1                  )
adcLn, = plt.plot        ( [],[],'r-o',linewidth=12, alpha = 0.3 ,label  = "adc")
adcAxe.grid              ( True                   )
adcAxe.set_ylim ( -1.5 ,1.5          )
adcAxe.set_xlim ( 0    ,(header["N"] ))

#----------------------ciaaFFT vs fft(adc)--------------------------
fftAxe        = fig.add_subplot ( 2,1,2 )
fftAxe.set_title("fft(ciaaFFT) vs fft(adc)",rotation = 0,fontsize = 10,va = "center")
fftLn,     = plt.plot ( [] ,[] ,'r-o' ,linewidth = 10  ,alpha = 0.3 ,label = "abs(FFT(adc))" )
#ciaaFftLn, = plt.plot ( [] ,[] ,'b-o' ,linewidth = 3 ,alpha = 0.8 ,label = "ciaaFFT filtered out" )
fftLg      = fftAxe.legend()
fftAxe.set_ylim ( 0,0.03 )#np.max(absFft))
#fftAxe.set_xlim ( -header["fs"]/2,header["fs"]/2-header["fs"]/header["N"])
fftAxe.grid     ( True   )
cutFrecZoneLn   = fftAxe.fill_between([0,0],100,-100,facecolor = "yellow",alpha = 0.2)

def findHeader(f,h):
    data=bytearray(b'12345678')
    while data!=h["pre"]:
        data+=f.read(1)
        if len(data)>len(h["pre"]):
            del data[0]
    h["id"]      = readInt4File(f,4)
    h["N" ]      = readInt4File(f)
    h["fs"]      = readInt4File(f)
    data=bytearray(b'1234')
    while data!=h["pos"]:
        data+=f.read(1)
        if len(data)>len(h["pos"]):
            del data[0]
    print({k:round(v,2) if isinstance(v,float) else v for k,v in h.items()})
    return h["id"],h["N"],h["fs"]

def readInt4File(f,size=2,sign=False):
    raw=f.read(1)
    while( len(raw) < size):
        raw+=f.read(1)
    return (int.from_bytes(raw,"little",signed=sign))

def flushStream(f,h):
    if(STREAM_FILE[1]=="serial"): #pregunto si estoy usando la bibioteca pyserial o un file
        f.flushInput()
    else:
        f.seek ( 2*(h["N"]+h["M"]-1),io.SEEK_END)

def readSamples(adc,synth,N,trigger=False,th=0):
    state="waitLow" if trigger else "sampling"
    i=0
    for t in range(N):
        sample = (readInt4File(streamFile,sign = True)*1.65)/(2**6*512)
        state,nextI= {
                "waitLow" : lambda sample,i: ("waitHigh",0) if sample<th else ("waitLow" ,0),
                "waitHigh": lambda sample,i: ("sampling",0) if sample>th else ("waitHigh",0),
                "sampling": lambda sample,i: ("sampling",i+1)
                }[state](sample,i)
        adc[i]=sample
        i=nextI

def update(t):
    global header
    flushStream ( streamFile,header )
    id,N,fs=findHeader ( streamFile,header )
    nData     = np.arange(0,N,1) #arranco con numeros enteros para evitar errores de float
    adc       = np.zeros(N)
    fft = np.zeros(N).astype(complex)
    tData     = nData/fs
    readSamples(adc,fft,N,False,0)

    adcAxe.set_xlim ( 0    ,N-1 )
    adcLn.set_data  ( nData ,adc  )

    fftAxe.set_xlim ( -fs/2,fs/2-fs/N)
    fData=nData*fs/N-fs/2
    fftDataAbs=np.abs(np.fft.fftshift(np.fft.fft(adc))/N)**2
    fftLn.set_data (fData ,fftDataAbs)

    #auto escala el eje y, pero no tan bajo
    fftAxe.set_ylim ( 0,np.clip(np.max(fftDataAbs),0.0001,100))


    return adcLn,  fftLn,

#seleccionar si usar la biblioteca pyserial o leer desde un archivo log.bin
if(STREAM_FILE[1]=="serial"):
    streamFile = serial.Serial(port=STREAM_FILE[0],baudrate=460800,timeout=None)
else:
    streamFile=open(STREAM_FILE[0],"rb",0)

ani=FuncAnimation(fig,update,10000,init_func=None,blit=True,interval=1,repeat=True)
plt.get_current_fig_manager().window.showMaximized() #para QT5
plt.show()
streamFile.close()
