import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sc
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig = plt.figure()
fig.suptitle('Spectrum average', fontsize=16)
fs          = 100
signalFrec1 = 20
signalFrec2 = 10
NN          = 10000
N           = 128 #numero de puntos en cada segmento. NN se estira un poco si no son multiplos

segments    = NN//N
residue     = NN-N*segments
if(residue>0):
    segments+=1
residue=N*segments-NN

NN    = NN+residue
nData = np.arange(0,NN,1)
#--------------------------------------
def x(n):
    return 0.1*np.sin(2*np.pi*signalFrec1*n)+0.5*np.random.normal(0,size=len(n))
#    return np.sin(2*np.pi*signalFrec1*n)+np.sin(2*np.pi*signalFrec2*n)

#--------------------------------------
tData     = nData/fs
xData     = np.concatenate((x(tData[:NN-residue]),np.zeros(residue)))
signalAxe = fig.add_subplot(4,1,1)
signalLn, = plt.plot(tData,xData,'b-',label = "signal",linewidth = 4,alpha = 0.2)
signalAxe.legend()
signalAxe.grid(True)
signalAxe.set_xlim(0,NN/fs)
signalAxe.set_ylim(np.min(xData)-0.2,np.max(xData)+0.2)
fftSignalZoneLn = signalAxe.fill_between([0,0],10,-10,facecolor="yellow",alpha=0.5)
#
tSegmentData   = nData[0:N]/fs
segmentData    = np.zeros(N)
fftSegmentAxe  = fig.add_subplot(4,1,2)
fSegmentData   = nData[:N]*(fs/(N-(N)%2))-fs/2
fftSegmentLn , = plt.plot([] ,[] ,'g-' ,label = "fft segment" ,linewidth = 3 ,alpha = 0.5)
fftSegmentAxe.legend()
fftSegmentAxe.grid(True)
fftSegmentAxe.set_xlim(-fs/2,fs/2-fs/N)
realtimefft=np.zeros(NN)
#
accAxe = fig.add_subplot(4,1,3)
accLn, = plt.plot([],[],'b-',label = "fft average",linewidth=3,alpha=0.5)
accData = np.zeros(N)
accAxe.legend()
accAxe.grid(True)
accAxe.set_xlim(-fs/2,fs/2-fs/N)
#
fftAxe          = fig.add_subplot(4,1,4)
fData           = nData*(fs/(NN-(NN)%2))-fs/2
fftDataAbs      = np.abs(np.fft.fftshift(np.fft.fft(xData)/NN))**2
fftLn         , = plt.plot(fData ,fftDataAbs ,'b-'  ,label = "fft total"   ,linewidth = 3 ,alpha = 0.2)

fOneSegmentData      = nData[:N]*(fs/(N-(N)%2))-fs/2
fftOneSegmentDataAbs = np.abs(np.fft.fftshift(np.fft.fft(xData[:N])/N))**2
fftOneSegmentLn ,    = plt.plot(fOneSegmentData ,fftOneSegmentDataAbs,'r-'  ,label = "fft segment"   ,linewidth = 3 ,alpha = 0.3)

fftAxe.legend()
fftAxe.grid(True)
fftAxe.set_xlim(-fs/2,fs/2-fs/NN)
fftAxe.set_ylim(np.min(fftOneSegmentDataAbs),np.max(fftOneSegmentDataAbs))
#--------------------------------------
def init():
    return fftLn,fftSignalZoneLn,fftSegmentLn,accLn,

def update(actualSegment):
    global accData
    segmentData=xData[actualSegment*N:(actualSegment+1)*N]
    fftSegmentDataAbs = np.abs(np.fft.fftshift(np.fft.fft(segmentData/N)))**2
    accData+=fftSegmentDataAbs/segments
    #accData=(accData+fftSegmentDataAbs)/2


    fftSegmentLn.set_data(fSegmentData,fftSegmentDataAbs)
    fftSignalZoneLn  = signalAxe.fill_between([tData[actualSegment*N],tData[(actualSegment+1)*N-1]],10,-10,facecolor = "yellow",alpha = 0.3)
    fftSegmentAxe.set_ylim(np.min(fftSegmentDataAbs),np.max(fftSegmentDataAbs))
    accLn.set_data(fSegmentData,accData)
    accAxe.set_ylim(np.min(accData),np.max(accData))
    return fftLn,fftSignalZoneLn,fftSegmentLn,accLn,

ani=FuncAnimation(fig,update,segments,init,interval=100 ,blit=True,repeat=False)
plt.get_current_fig_manager().window.showMaximized()
plt.show()
