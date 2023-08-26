import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sc
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig        = plt.figure()
fig.suptitle('Deconvolucion', fontsize=16)
fs          = 100
N           = 100
signalFrec1 = 2
signalFrec2 = 10

firData,        = np.load("../utils/low_pass.npy").astype(float)
M               = len(firData)
nData           = np.arange(0,N+M-1,1)
nDataNegative   = np.arange(-(M-1),N+M-1,1) #agrega los M-1 pero tambien otross M-1 para calcular el y[0]
firExtendedData = np.concatenate((firData,np.zeros(N-1)))

HData=np.fft.fft(firExtendedData)

#descomentar estas dos para 'romper' el h y ver como la deconvolucion lo repara
HData[10:15]=1
firExtendedData=np.fft.ifft(HData)
firData=firExtendedData[:M]
#--------------------------------------
def x(n):
    #    return np.sin(2*np.pi*10*n)+np.sin(2*np.pi*5*n)
    out=np.zeros(N)
    for i in range(10):
        out[i]=i
    for i in range(10):
        out[10+i]=10-i
    return out

tData          = nData/fs
fData          = nData*(fs/(N+M-1))-fs/2
xData          = np.zeros(N+M-1)
xData[:N]     += x(tData[:N])
tDataNegative  = nDataNegative/fs
xDataNegative  = np.concatenate((np.zeros(M-1),xData))

#----------OUTPUT SIDE vs NUMPY CONVOLVE----------------------------
xAxe  = fig.add_subplot(3,3,1)
xAxe.set_title("Convolucion de x con h",rotation=0,fontsize=10,va="center")
xLn,  = plt.plot(tData,xData,'b-',label="x",linewidth=3,alpha=0.8)
xAxe.legend()
xAxe.grid(True)

hAxe  = fig.add_subplot(3,3,4)
hLn,  = plt.plot(tData[:M],np.real(firData),'g-',label="h",linewidth=2,alpha=0.8)
hAxe.legend()
hAxe.grid(True)
hAxe.set_xlim(0,(N+M-2)/fs)
#
yAxe  = fig.add_subplot(3,3,7)

yData = np.convolve(xData[0:N],firData)
yLn,  = plt.plot(tData,np.real(yData),'r-',label = "y",linewidth = 2,alpha = 0.8)
yAxe.legend()
yAxe.grid(True)
##------FFT(x) * FFT(h)--------------------------------
XAxe  = fig.add_subplot(3,3,2)
XAxe.set_title("DFT(x)",rotation=0,fontsize=10,va="center")
XData = np.fft.fft(xData)

circularXData=np.fft.fftshift(XData)
XLn,  = plt.plot(fData,np.abs(circularXData),'b-',label="X",linewidth=2,alpha=0.8)
XAxe.legend()
XAxe.grid(True)

circularHData=np.fft.fftshift(HData)
HAxe  = fig.add_subplot(3,3,5)
HLn,  = plt.plot(fData,np.abs(circularHData),'g-',label="H",linewidth=2,alpha=0.8)
HAxe.legend()
HAxe.grid(True)

YAxe  = fig.add_subplot(3,3,8)
YData=XData*HData
circularYData=np.fft.fftshift(YData)
YLn,    = plt.plot(fData,np.abs(circularYData),'r-',label = "Y",linewidth=2,alpha=0.8)
YAxe.legend()
YAxe.grid(True)

#----------DECONVOLUCION----------------------------
deconvAxe     = fig.add_subplot(3,3,3)
deconvAxe.set_title("Devonvolucion",rotation=0,fontsize=10,va="center")
deconvLn,     = plt.plot(tData,np.real(yData),'b-',label = "input",linewidth=2,alpha=0.8)
deconvAxe.legend()
deconvAxe.grid(True)
#
HinvData         = 1/HData
circularHinvData = np.fft.fftshift(HinvData)
HinvAxe          = fig.add_subplot(3,3,6)
HinvLn,          = plt.plot(fData,np.abs(circularHinvData),'g-',label = "Hinv",linewidth = 2,alpha = 0.8)
HinvAxe.legend()
HinvAxe.grid(True)
#
xdeconvData = np.real(np.fft.ifft(YData*HinvData))
xdeconvAxe  = fig.add_subplot(3,3,9)
xdeconvLn,  = plt.plot(tData,xdeconvData,'r-',label = "x devonv",linewidth = 2,alpha = 0.8)

plt.get_current_fig_manager().window.showMaximized()
plt.show()
