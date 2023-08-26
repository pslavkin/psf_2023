#!python3
import numpy as np
import matplotlib.pyplot as plt
from   matplotlib.animation import FuncAnimation
import os
import io
import serial

STREAM_FILE=("/dev/ttyUSB3","serial")
#STREAM_FILE=("log.bin","file")

FFT_LENGTH=512
CHORD_WIDTH=2
CHORD_TUNE=0.4
chordsFrecs=[82.41 ,110.00 ,146.83 ,196.00 ,246.94 ,329.63]
chordsNames=['MI','LA','RE','SOL','SI','MI']
chordsColors=["green","yellow","red","blue","magenta","black"]

header = { "pre": b"*header*", "id": 0, "N": 100, "fs": 1000, "maxValue":0,"maxIndex":0, "pos":b"end*" }
fig    = plt.figure ( 1 )
fig.suptitle('Guitar Tunner con la CIAA', fontsize=16)

#--------------------------ADC--------------------------
adcAxe = fig.add_subplot ( 3,1,1                  )
adcLn, = plt.plot        ( [],[],'r-o',linewidth=12, alpha = 0.3 ,label  = "adc")
adcAxe.grid              ( True                   )
adcAxe.set_ylim ( -1.5 ,1.5          )
adcAxe.set_xlim ( 0    ,(header["N"] ))

#----------------------ciaaFFT & fft(adc)--------------------------
fftAxe        = fig.add_subplot ( 3,1,3 )
fftAxe.set_title("fft(ciaaFFT) vs fft(adc)",rotation = 0,fontsize = 10,va = "center")
fftLn,     = plt.plot ( [] ,[] ,'r-o' ,linewidth = 10  ,alpha = 0.3 ,label = "abs(FFT(adc))" )
ciaaFftLn, = plt.plot ( [] ,[] ,'b-o' ,linewidth = 3 ,alpha = 0.8 ,label = "ciaaFFT" )
ciaaMaxLn, = plt.plot ( [] ,[] ,'k-o' ,linewidth = 3 ,alpha = 0.8 ,label = "maxLine")
fftLg      = fftAxe.legend(loc='upper right',prop={'size': 10})
#fftAxe.set_ylim ( 0,0.02 )#np.max(absFft))
fftAxe.set_xlim ( 0,header["fs"]/2-header["fs"]/header["N"])
fftAxe.grid     ( True   )
cutFrecZoneLn   = fftAxe.fill_between([0,0],100,-100,facecolor = "yellow",alpha = 0.2)
for i in range(6):
    fftAxe.fill_between([chordsFrecs[i]-CHORD_WIDTH,chordsFrecs[i]+CHORD_WIDTH],-10,2000,facecolor = chordsColors[i],alpha=0.4)
#-----------------------ciaaMaxLine------------------------------------------------------
chordLn=[]
chordAxe=[]
for i in range(6):
    chordAxe.append(fig.add_subplot ( 3,6,7+i ))
    chordAxe[i].set_xlim ( chordsFrecs[i]-CHORD_WIDTH  ,chordsFrecs[i]+CHORD_WIDTH   )
    chordAxe[i].set_ylim ( 0  ,10   )
    plt.axvline(chordsFrecs[i])
    chordLn.append(plt.plot ( 0,0,'k',label="{}:{}".format(chordsNames[i],chordsFrecs[i]))[0])
    chordAxe[i].legend(loc='upper right',prop={'size': 14})
    chordAxe[i].grid ( True )


def findHeader(f,h):
    data=bytearray(b'12345678')
    while data!=h["pre"]:
        data+=f.read(1)
        if len(data)>len(h["pre"]):
            del data[0]
    h["id"]      = readInt4File(f,4)
    h["N" ]      = readInt4File(f)
    h["fs"]      = readInt4File(f)
    h["maxValue"]  = (readInt4File(streamFile,sign = True)*1.65)/(2**6*512)
    h["maxIndex"] = (readInt4File(f,4)/(1000*FFT_LENGTH))*header["fs"]  #/FFT_LENGTH-header["fs"]/2#*header["fs"])/(1000*FFT_LENGTH)
    data=bytearray(b'1234')
    while data!=h["pos"]:
        data+=f.read(1)
        if len(data)>len(h["pos"]):
            del data[0]
    print({k:round(v,2) if isinstance(v,float) else v for k,v in h.items()})
    return h["id"],h["N"],h["fs"],h["maxValue"],h["maxIndex"]

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
        sample  = (readInt4File(streamFile,sign = True)*1.65)/(2**6*512)
        ciaaFFT = (readInt4File(streamFile,sign = True)*1.65)/(2**6*512)
        state,nextI= {
                "waitLow" : lambda sample,i: ("waitHigh",0) if sample<th else ("waitLow" ,0),
                "waitHigh": lambda sample,i: ("sampling",0) if sample>th else ("waitHigh",0),
                "sampling": lambda sample,i: ("sampling",i+1)
                }[state](sample,i)
        adc[i]   = sample
        synth[i] = ciaaFFT
        i        = nextI

def update(t):
    global header
    flushStream ( streamFile,header )
    id,N,fs,maxValue,maxIndex=findHeader ( streamFile,header )
    nData     = np.arange(0,N,1) #arranco con numeros enteros para evitar errores de float
    adc       = np.zeros(N)
    ciaaFFT   = np.zeros(N)
    tData     = nData/fs
    readSamples(adc,ciaaFFT,N,False,0)

#    adcAxe.set_xlim ( 0    ,N-1 )
    adcLn.set_data  ( nData ,adc  )

    fData=nData*fs/N-fs/2
    fftDataAbs=np.abs(np.fft.fftshift(np.fft.fft(adc))/N)**2
    fftLn.set_data (fData ,fftDataAbs)

    ciaaFftLn.set_data (fData ,np.fft.fftshift(ciaaFFT))
    ciaaMaxLn.set_data(maxIndex,maxValue)


    #auto escala el eje y, pero no tan bajo
    fftAxe.set_ylim ( 0,0.4)#np.clip(np.max((maxValue,np.max(ciaaFFT))),0.01,10)+0.01)
    ciaaMaxLn.set_label("frec:{0:.2f}".format(maxIndex))
    fftLg  = fftAxe.legend(loc='upper right',prop={'size': 16})

    multiIndex=np.full(10,maxIndex)
    multiData=np.arange(0,10,1)
    for i in range(len(chordsFrecs)):
        if maxIndex>(chordsFrecs[i]-CHORD_TUNE) and maxIndex<(chordsFrecs[i]+CHORD_TUNE):
            chordLn[i].set_label('OK!')
        else:
            chordLn[i].set_label("{}:{}".format(chordsNames[i],chordsFrecs[i]))
        chordLg  = chordAxe[i].legend(loc='upper right',prop={'size': 16})

    for i in chordLn:
        i.set_data(multiIndex,multiData)
        i.set_data(multiIndex,multiData)
        i.set_data(multiIndex,multiData)
        i.set_data(multiIndex,multiData)
        i.set_data(multiIndex,multiData)
        i.set_data(multiIndex,multiData)

    return adcLn,  fftLn, ciaaFftLn,ciaaMaxLn

#seleccionar si usar la biblioteca pyserial o leer desde un archivo log.bin
if(STREAM_FILE[1]=="serial"):
    streamFile = serial.Serial(port=STREAM_FILE[0],baudrate=460800,timeout=None)
else:
    streamFile=open(STREAM_FILE[0],"rb",0)

ani=FuncAnimation(fig,update,10000,init_func=None,blit=False,interval=10,repeat=True)
plt.get_current_fig_manager().window.showMaximized() #para QT5
plt.show()
streamFile.close()
