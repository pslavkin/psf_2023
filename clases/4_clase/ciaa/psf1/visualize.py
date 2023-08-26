#!python3
import numpy as np
import matplotlib.pyplot as plt
from   matplotlib.animation import FuncAnimation
import os
import io
import serial

STREAM_FILE=("/dev/ttyUSB3","serial")
#STREAM_FILE=("log.bin","file")

header = { "head": b"head", "id": 0, "N": 128, "fs": 10000, "cutFrec":0,"tail":b"tail" }
fig    = plt.figure ( 1 )
fig.suptitle('Transformada inversa de Fourier', fontsize=16)

#--------------------------ADC--------------------------
adcAxe = fig.add_subplot ( 3,1,1                  )
adcLn, = plt.plot        ( [],[],'r-o',linewidth=12, alpha = 0.3 ,label  = "adc")
adcAxe.grid              ( True                   )
adcAxe.set_ylim          ( -1.2 ,1.2              )

#----------------------ciaaSynth vs ifft(fft(adc))--------------------------
synthAxe     = fig.add_subplot ( 3,1,2                                 )
synthAxe.set_title("ciaaSynth vs ifft(fft(adc))",rotation=0,fontsize=10,va="center")
ifftLn,      = plt.plot ( [] ,[] ,'r-' ,linewidth = 2  ,alpha = 0.3 ,label  = "IFFT(FFT(adc))")
ciaaSynthLn, = plt.plot ( [] ,[] ,'b-' ,linewidth = 12 ,alpha = 0.4  ,label = "ciaaSynth" )
synthLg=synthAxe.legend()
synthAxe.grid     ( True      )
synthAxe.set_ylim ( -1.2 ,1.2 )

#----------------------fft(ciaaSynth) vs fft(adc)--------------------------
fftAxe        = fig.add_subplot ( 3,1,3 )
fftAxe.set_title("fft(ciaaSynth) vs fft(adc)",rotation = 0,fontsize = 10,va = "center")
fftLn,     = plt.plot ( [] ,[] ,'r-o' ,linewidth = 2  ,alpha = 0.3 ,label = "abs(FFT(adc))" )
ciaaFftLn, = plt.plot ( [] ,[] ,'b-o' ,linewidth = 12 ,alpha = 0.5 ,label = "abs(FFT(ciaaSynth))" )
fftLg      = fftAxe.legend()
fftAxe.set_ylim ( 0,0.05 )#np.max(absFft))
fftAxe.grid     ( True   )
cutFrecZoneLn   = fftAxe.fill_between([0,0],100,-100,facecolor = "yellow",alpha = 0.2)

def findHeader(f,h):
    data=bytearray(b'1234')
    while data!=h["head"]:
        data+=f.read(1)
        if len(data)>len(h["head"]):
            del data[0]
    h["id"]      = readInt4File(f,4)
    h["N" ]      = readInt4File(f)
    h["fs"]      = readInt4File(f)
    h["cutFrec"] = readInt4File(f)
    data=bytearray(b'1234')
    while data!=h["tail"]:
        data+=f.read(1)
        if len(data)>len(h["tail"]):
            del data[0]
    print({k:round(v,2) if isinstance(v,float) else v for k,v in h.items()})
    return h["id"],h["N"],h["fs"],h["cutFrec"]

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

def readSamples(adc,synth,N,trigger=False,th=0):
    state="waitLow" if trigger else "sampling"
    i=0
    for t in range(N):
        sample = (readInt4File(streamFile,sign = True)*1.65)/(2**6*512)
        #part real plus imag
        ciaaSynth = (readInt4File(streamFile,sign = True)*1.65*2**(np.log2(N)-6))/512 #wah?! es que segun el N la salida de la cfft de cmsis te corre el q15. la cuante da que para 128 hay que multiplicar por 1 , 256:2, 512:3, etc.
        state,nextI= {
                "waitLow" : lambda sample,i: ("waitHigh",0) if sample<th else ("waitLow" ,0),
                "waitHigh": lambda sample,i: ("sampling",0) if sample>th else ("waitHigh",0),
                "sampling": lambda sample,i: ("sampling",i+1)
                }[state](sample,i)
        adc[i]=sample
        synth[i]=ciaaSynth
        i=nextI

def update(t):
    global header
    flushStream ( streamFile,header )
    id,N,fs,cutFrec=findHeader ( streamFile,header )
    nData     = np.arange(0,N,1) #arranco con numeros enteros para evitar errores de float
    adc       = np.zeros(N)
    ciaaSynth = np.zeros(N).astype(complex)
    tData     = nData/fs
    readSamples(adc,ciaaSynth,N,False,0)

    adcAxe.set_xlim ( 0    ,N/fs )
    adcLn.set_data  ( tData ,adc  )

    synthAxe.set_xlim    ( 0 ,N/fs                                   )
    ciaaSynthLn.set_data ( tData ,ciaaSynth                          )
    ifftLn.set_data      ( tData ,np.real(np.fft.ifft(np.fft.fft(adc ))))

    fftAxe.set_xlim ( -fs/2,fs/2-fs/N)
    fData=nData*fs/N-fs/2
    ciaaFftLn.set_data (fData ,np.abs(np.fft.fftshift(np.fft.fft(ciaaSynth))/N)**2)
    fftLn.set_data (fData ,np.abs(np.fft.fftshift(np.fft.fft(adc))/N)**2)

    cutFrecZoneLn = fftAxe.fill_between([-cutFrec,cutFrec],100,-100,facecolor="yellow",alpha=0.5)

    return adcLn, ciaaSynthLn, ifftLn, ciaaFftLn, fftLn, cutFrecZoneLn

#seleccionar si usar la biblioteca pyserial o leer desde un archivo log.bin
if(STREAM_FILE[1]=="serial"):
    streamFile = serial.Serial(port=STREAM_FILE[0],baudrate=460800,timeout=None)
else:
    streamFile=open(STREAM_FILE[0],"rb",0)

ani=FuncAnimation(fig,update,10000,init_func=None,blit=True,interval=1,repeat=True)
plt.get_current_fig_manager().window.showMaximized() #para QT5
plt.show()
streamFile.close()
