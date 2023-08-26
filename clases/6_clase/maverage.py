import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sc
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig        = plt.figure()
fig.suptitle('Filtrado FIR por convolucion', fontsize=16)
fs          = 100
N           = 180
signalFrec1 = 2
signalFrec2 = 10

#kernel="../utils/hi_pass_short.npy"
kernel="../utils/average_11_stages1.npy"
#kernel="../utils/average_11_stages2.npy"
#kernel="../utils/average_11_stages3.npy"
#kernel="../utils/low_pass_5hz_fs100.npy"
#kernel="../utils/low_pass.npy"
#kernel="../utils/hi_pass.npy"

firData,=np.load(kernel).astype(float)
#firData=np.insert(firData,0,firData[-1]) #ojo que pydfa me guarda 1 dato menos...
M = len(firData)

nData         = np.arange(0,N+M-1,1)
nDataNegative = np.arange(-(M-1),N+M-1,1) #agrega los M-1 pero tambien otross M-1 para calcular el y[0]
firExtendedData=np.concatenate((firData,np.zeros(N-1)))
#--------------------------------------
def noise(n):
    return np.random.normal(0,0.2,n)

def x(n):
#    return 1*sc.sawtooth(2*np.pi*2*n,0.5)
    return np.sin(2*np.pi*signalFrec1*n)+noise(len(n))
#    return np.sin(2*np.pi*signalFrec1*n)+np.sin(2*np.pi*signalFrec2*n)

tData          = nData/fs
fData          = nData*(fs/((N+M-1)-(N+M-1)%2))-fs/2
xData          = np.zeros(N+M-1)
xData[:N]     += x(tData[:N])
tDataNegative  = nDataNegative/fs
xDataNegative  = np.concatenate((np.zeros(M-1),xData))
#----------OUTPUT SIDE vs NUMPY CONVOLVE----------------------------
signalAxe  = fig.add_subplot(3,2,1)
signalAxe.set_title("Output side conv",rotation=0,fontsize=10,va="center")
signalLn,  = plt.plot(tData,xData,'b-o',label="x",linewidth=3,alpha=0.3)
signalAxe.legend()
signalAxe.grid(True)
signalAxe.set_xlim(0,(N+M-2)/fs)
signalAxe.set_ylim(np.min(xData)-0.2,np.max(xData)+0.2)
convZoneLn = signalAxe.fill_between([0,0],10,-10,facecolor="yellow",alpha=0.5)

firAxe  = fig.add_subplot(3,2,3)
firAxe.set_title(kernel,rotation=0,fontsize=10,va="center")
firLn,  = plt.plot([],[],'g-o',label="h",linewidth=3,alpha=0.3)
firAxe.legend()
firAxe.grid(True)
firAxe.set_xlim(0,(N+M-2)/fs)
firAxe.set_ylim(np.min(firData),np.max(firData))

convAxe         = fig.add_subplot(3,2,5)
convolveData    = np.convolve(xData[0:N],firData)
convLn,         = plt.plot(tData,convolveData,'r-',label = "numpy",linewidth=16,alpha=0.2)
realtimeConvLn, = plt.plot([],[],'r-o',label="conv")
convAxe.legend()
convAxe.grid(True)
convAxe.set_xlim(0,(N+M-2)/fs)

#------FFT(x) * FFT(h)--------------------------------
XAxe  = fig.add_subplot(3,2,2)
XAxe.set_title("IDFT (DFT(x) x DFT(h))",rotation=0,fontsize=10,va="center")
XData = np.fft.fft(xData)

circularXData=np.fft.fftshift(XData)
XLn,  = plt.plot(fData,np.abs(circularXData),'b-',label="X",linewidth=3,alpha=0.5)
XAxe.legend()
XAxe.grid(True)
XAxe.set_xlim(-fs/2,fs/2)

HData         = np.fft.fft(firExtendedData)
circularHData = np.fft.fftshift(HData)
HAxe          = fig.add_subplot(3,2,4)
HLn,          = plt.plot(fData,np.abs(circularHData),'g-',label = "H",linewidth = 3,alpha = 0.5)
HAxe.legend()
HAxe.grid(True)
HAxe.set_xlim(-fs/2,fs/2)

YAxe  = fig.add_subplot(3,2,6)
YData=XData*HData
circularYData=np.fft.fftshift(YData)
YLn,    = plt.plot(fData,np.abs(circularYData),'r-',label = "Y",linewidth=3,alpha=0.8)
YfftLn, = plt.plot([],[],'b-',label = "fft(conv)",linewidth=6,alpha=0.3)
YAxe.legend()
YAxe.grid(True)
YAxe.set_ylim(np.min(np.abs(circularXData)),np.max(np.abs(circularXData)))
YAxe.set_xlim(-fs/2,fs/2)

def init():
    global yData,realtimeConv
    yData        = np.zeros(N+M-1)
    realtimeConv = np.zeros(N+M-1)
    convZoneLn   = signalAxe.fill_between([0,0],10,-10,facecolor = "yellow",alpha = 0.5)
    return XLn,HLn,YLn,YfftLn,firLn,realtimeConvLn,convZoneLn,

def update(i):
    global yData,b,realtimeConv
    if i<=N-1:

        hData=np.zeros(N+M-1)
        hData[i:i+M]=firData
        yData+=hData*xData[i]

        YfftData=np.fft.fft(yData)
        circularYfftData=np.fft.fftshift(YfftData)
        YfftLn.set_data(fData,np.abs(circularYfftData))

    firLn.set_data(tDataNegative[i:i+M],firData[::-1])
    realtimeConv[i]=np.sum(xDataNegative[i:i+M]*firData[::-1])
    realtimeConvLn.set_data(tData,realtimeConv)
    convZoneLn = signalAxe.fill_between([tDataNegative[i],tDataNegative[i+M-1]],100,-100,facecolor="yellow",alpha=0.5)

    return XLn,HLn,YLn,YfftLn,firLn,realtimeConvLn,convZoneLn,

ani=FuncAnimation(fig,update,N+M-1,init,interval=100 ,blit=True,repeat=True)
plt.get_current_fig_manager().window.showMaximized()
plt.show()

