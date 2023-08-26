import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sc
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig             = plt.figure()
fig.suptitle('Overlap and add en t', fontsize=16)
fs          = 100
signalFrec1 = 2
signalFrec2 = 10
NN          = 2000
N           = 206 #numero de puntos en cada segmento. NN se estira un poco si no son multiplos
segments    = NN//N
residue     = NN-N*segments
if(residue>0):
    segments+=1
residue=N*segments-NN


#firData,    = np.load("../utils/average_11_stages1.npy").astype(float)
firData, = np.load("../utils/low_pass_5hz.npy").astype(float)

M                    = len(firData)
NN                   = NN+residue
nData                = np.arange(0,NN+M-1,1)
nSegmentDataNegative = np.arange(-(M-1),NN+M-1,1)
#--------------------------------------
def x(n):
    return np.sin(2*np.pi*signalFrec1*n)+np.sin(2*np.pi*signalFrec2*n)

#--------------------------------------
tData=nData/fs
xData=np.concatenate((x(tData[:NN-residue]),np.zeros(residue+M-1)))
signalAxe  = fig.add_subplot(4,1,1)
signalLn,  = plt.plot(tData,xData,'b-o',label="signal",linewidth=4,alpha=0.2)
signalAxe.legend()
signalAxe.grid(True)
signalAxe.set_xlim(0,(NN+M-2)/fs)
signalAxe.set_ylim(np.min(xData)-0.2,np.max(xData)+0.2)
convSignalZoneLn = signalAxe.fill_between([0,0],10,-10,facecolor="yellow",alpha=0.5)
#
tSegmentData         = nData[0:N+M-1]/fs
tSegmentDataNegative = nSegmentDataNegative/fs
segmentData          = np.zeros(N+M-1)
#
actualSegment=0
segmentAxe  = fig.add_subplot(4,1,2)
segmentLn,  = plt.plot([],[],'b-o',label="segment")
segmentAxe.legend()
segmentAxe.grid(True)
segmentAxe.set_xlim(0,(N+M-2)/fs)
segmentAxe.set_ylim(np.min(xData)-0.2,np.max(xData)+0.2)
segmentSignalZoneLn = segmentAxe.fill_between([0,0],10,-10,facecolor="yellow",alpha=0.5)
##
firAxe  = fig.add_subplot(4,1,3)
firLn,  = plt.plot([],[],'b-o',label="fir kernel")
firAxe.legend()
firAxe.grid(True)
firAxe.set_xlim(0,(N+M-2)/fs)
firAxe.set_ylim(np.min(firData)-0.01,np.max(firData)+0.01)
##
convAxe         = fig.add_subplot(4,1,4)
convolveData    = np.convolve(xData[:NN],firData)
convLn,         = plt.plot(tData,convolveData,'b-',label = "conv",linewidth=12,alpha=0.3)
realtimeConvLn, = plt.plot([],[],'r-o',label='segment conv',linewidth=2,alpha=0.8)
convAxe.legend()
convAxe.grid(True)
convAxe.set_xlim(0,(NN+M-2)/fs)
convAxe.set_ylim(np.min(convolveData),np.max(convolveData))
convSegmentZoneLn = convAxe.fill_between([0,0],10,-10,facecolor="yellow",alpha=0.3)
realtimeConv=np.zeros(NN+M-1)
###--------------------------------------
#
def init():
    global yData,realtimeConv
#    realtimeConv=np.zeros(N+M-1)
    convZoneLn = signalAxe.fill_between([0,0],10,-10,facecolor="yellow",alpha=0.51)
    return firLn,realtimeConvLn,convSegmentZoneLn,convSignalZoneLn,segmentLn,segmentSignalZoneLn
#
def update(i):
    global yData,b,realtimeConv,actualSegment
#
    segmentData[:N]=xData[actualSegment*N:(actualSegment+1)*N]
    segmentLn.set_data(tSegmentData,segmentData)
#
    segmentDataNegative=np.concatenate((np.zeros(M-1),segmentData))
    firLn.set_data(tSegmentDataNegative[i:i+M],firData[::-1])
    realtimeConv[actualSegment*N+i]+=np.sum(segmentDataNegative[i:i+M]*firData[::-1])
    realtimeConvLn.set_data(tData,realtimeConv)
    convSegmentZoneLn = convAxe.fill_between([tData[actualSegment*N],tData[(actualSegment+1)*N+M-2]],10,-10,facecolor = "yellow",alpha = 0.3)
    convSignalZoneLn  = signalAxe.fill_between([tData[actualSegment*N],tData[(actualSegment+1)*N-1]],10,-10,facecolor = "yellow",alpha = 0.3)
    segmentSignalZoneLn = segmentAxe.fill_between([0,tData[N-1]],10,-10,facecolor="yellow",alpha=0.3)
    if i==N+M-2:
        if actualSegment<(segments-1):
            actualSegment+=1
        else:
            ani.event_source.stop()
    return firLn,realtimeConvLn,convSegmentZoneLn,convSignalZoneLn,segmentLn,segmentSignalZoneLn
#
ani=FuncAnimation(fig,update,N+M-1,init,interval=10 ,blit=True,repeat=True)
plt.get_current_fig_manager().window.showMaximized()
plt.show()
