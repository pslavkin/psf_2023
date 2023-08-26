import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sc
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig        = plt.figure()
fig.suptitle('Teorema de la convolucion', fontsize=16)
fs          = 100
N           = 100
signalFrec1 = 2
signalFrec2 = 10

#firData,=np.load("../utils/hi_pass_short.npy").astype(float)
firData,=np.load("../utils/low_pass.npy").astype(float)
#firData,=np.load("../utils/hi_pass.npy").astype(float)
firData=np.insert(firData,0,firData[-1]) #ojo que pydfa me guarda 1 dato menos...
M          = len(firData)

nData         = np.arange(0,N+M-1,1)
nDataNegative = np.arange(-(M-1),N+M-1,1) #agrega los M-1 pero tambien otross M-1 para calcular el y[0]
firExtendedData=np.concatenate((firData,np.zeros(N-1)))
#--------------------------------------
def x(n):
#    return 1*sc.sawtooth(2*np.pi*2*n,0.5)
    return np.sin(2*np.pi*signalFrec1*n)+np.sin(2*np.pi*signalFrec2*n)

tData=nData/fs
fData=nData*(fs/(N+M-1))-fs/2
xData=np.zeros(N+M-1)
xData[:N]+=x(tData[:N])
tDataNegative=nDataNegative/fs
xDataNegative=np.concatenate((np.zeros(M-1),xData))
#----------OUTPUT SIDE vs NUMPY CONVOLVE----------------------------
signalAxe  = fig.add_subplot(3,3,1)
signalAxe.set_title("Output side conv",rotation=0,fontsize=10,va="center")
signalLn,  = plt.plot(tData,xData,'b-o',label="x",linewidth=3,alpha=0.3)
signalAxe.legend()
signalAxe.grid(True)
signalAxe.set_xlim(0,(N+M-2)/fs)
signalAxe.set_ylim(np.min(xData)-0.2,np.max(xData)+0.2)
convZoneLn = signalAxe.fill_between([0,0],10,-10,facecolor="yellow",alpha=0.5)

firAxe  = fig.add_subplot(3,3,4)
firLn,  = plt.plot([],[],'g-o',label="h",linewidth=3,alpha=0.3)
firAxe.legend()
firAxe.grid(True)
firAxe.set_xlim(0,(N+M-2)/fs)
firAxe.set_ylim(np.min(firData),np.max(firData))

convAxe         = fig.add_subplot(3,3,7)
convolveData    = np.convolve(xData[0:N],firData)
convLn,         = plt.plot(tData,convolveData,'r-',label = "numpy",linewidth = 16,alpha = 0.2)
convPointLn,    = plt.plot([] ,[] ,'ko' ,label = 'point',linewidth = 3 ,alpha = 1)
realtimeConvLn, = plt.plot([] ,[] ,'r-o' ,label = "conv" ,linewidth = 3 ,alpha = 0.2)
convAxe.legend()
convAxe.grid(True)
convAxe.set_xlim(0,(N+M-2)/fs)

#----------INPUT SIDE vs IFFT(FFT)----------------------------
xAxe     = fig.add_subplot(3,3,2)
xAxe.set_title("Input side conv",rotation=0,fontsize=10,va="center")
xLn,     = plt.plot(tData,xData,'b-o',label = "x",linewidth=3,alpha=0.3)
xAxe.legend()
xAxe.grid(True)
xAxe.set_xlim(0,(N+M-2)/fs)
xAxe.set_ylim(np.min(xData)*1.1,np.max(xData)*1.1)
xZoneLn = xAxe.fill_between([0,0],10,-10,facecolor="yellow",alpha=0.5)

hAxe  = fig.add_subplot(3,3,5)
hLn,  = plt.plot([],[],'g-o',label="h",linewidth=3,alpha=0.3)
hAxe.legend()
hAxe.grid(True)
hAxe.set_xlim(0,(N+M-2)/fs)
hAxe.set_ylim(-0.1,0.1)

yAxe     = fig.add_subplot(3,3,8)

yifftData = np.real(np.fft.ifft(np.fft.fft(xData)*np.fft.fft(firExtendedData)))
yifftLn, = plt.plot(tData,yifftData,'r-',label = "ifft",linewidth=16,alpha=0.3)
yLn,     = plt.plot([],[],'r-o',label = "y",linewidth=1,alpha=0.8)
yAxe.legend()
yAxe.grid(True)
yAxe.set_xlim(0,(N+M-2)/fs)
yAxe.set_ylim(np.min(convolveData)-0.1,np.max(convolveData)+0.1)
#yAxe.set_ylim(0,15)
yData=np.zeros(N+M-1)

#------FFT(x) * FFT(h)--------------------------------
XAxe  = fig.add_subplot(3,3,3)
XAxe.set_title("IDFT (DFT(x) x DFT(h))",rotation=0,fontsize=10,va="center")
XData = np.fft.fft(xData)
print(len(XData))

circularXData=np.fft.fftshift(XData)
XLn,  = plt.plot(fData,np.abs(circularXData),'b-',label="X",linewidth=3,alpha=0.5)
XAxe.legend()
XAxe.grid(True)
XAxe.set_xlim(-fs/2,fs/2-fs/N)

HData=np.fft.fft(firExtendedData)
circularHData=np.fft.fftshift(HData)
HAxe  = fig.add_subplot(3,3,6)
HLn,  = plt.plot(fData,np.abs(circularHData),'g-',label="H",linewidth=3,alpha=0.5)
HAxe.legend()
HAxe.grid(True)
HAxe.set_xlim(-fs/2,fs/2-fs/N)

YAxe  = fig.add_subplot(3,3,9)
YData=XData*HData
circularYData=np.fft.fftshift(YData)
YLn,    = plt.plot(fData,np.abs(circularYData),'r-',label = "Y",linewidth=3,alpha=0.8)
YfftLn, = plt.plot([],[],'b-',label = "fft(conv)",linewidth=10,alpha=0.3)
YAxe.legend()
YAxe.grid(True)
YAxe.set_ylim(np.min(np.abs(circularXData)),np.max(np.abs(circularXData)))
YAxe.set_xlim(-fs/2,fs/2-fs/N)

def init():
    global yData,realtimeConv,xZoneLn
    yData        = np.zeros(N+M-1)
    realtimeConv = np.zeros(N+M-1)
    convZoneLn   = signalAxe.fill_between([0,0],10,-10,facecolor = "yellow",alpha = 0.5)
    xZoneLn      = xAxe.fill_between     ([0,0],10,-10,facecolor = "yellow",alpha = 0.5)
    return yLn,convPointLn,hLn,XLn,HLn,YLn,YfftLn,firLn,realtimeConvLn,convZoneLn,xZoneLn

def update(i):
    global yData,b,realtimeConv,xZoneLn
    #input()
    if i<=N-1:
        hLn.set_data(tData[i:i+M],firData*xData[i])
        xZoneLn = xAxe.fill_between([tData[i],tData[i+M-1]],10,-10,facecolor="yellow",alpha=0.5)

        #input side convolution
        hData=np.zeros(N+M-1)
        hData[i:i+M]=firData
        yData+=hData*xData[i]
        yLn.set_data(tData,yData)

        #fft a partir de la convolicion input side
        YfftData=np.fft.fft(yData)
        YfftLn.set_data(fData,np.abs(np.fft.fftshift(YfftData)))

    #ouput side convolution
    firLn.set_data(tDataNegative[i:i+M],firData[::-1])
    realtimeConv[i]=np.sum(xDataNegative[i:i+M]*firData[::-1])
    realtimeConvLn.set_data(tData,realtimeConv)
    convPointLn.set_data(tData[i],realtimeConv[i])
    convZoneLn = signalAxe.fill_between([tDataNegative[i],tDataNegative[i+M-1]],100,-100,facecolor="yellow",alpha=0.5)

    return yLn,convPointLn,hLn,XLn,HLn,YLn,YfftLn,firLn,realtimeConvLn,convZoneLn,xZoneLn

ani=FuncAnimation(fig,update,N+M-1,init,interval=10 ,blit=True,repeat=True)
plt.get_current_fig_manager().window.showMaximized()
plt.show()
