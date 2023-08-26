import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sc
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig         = plt.figure()
fs          = 100
N           = 100
signalFrec1 = 2
signalFrec2 = 10
convStages  = 5
fig.suptitle('Filtrado FIR np.convolve multiples etapas: {}'.format(convStages), fontsize=16)

#kernel="../utils/hi_pass_short.npy"
kernel="../utils/average_11_stages1.npy"
#kernel="../utils/average_11_stages2.npy"
#kernel="../utils/average_11_stages3.npy"
#kernel="../utils/low_pass_5hz.npy"
#kernel="../utils/low_pass_10_fs100.npy"
#kernel="../utils/low_pass_6_fs100.npy"
#kernel="../utils/low_pass.npy"
#kernel="../utils/hi_pass.npy"

firData,=np.load(kernel).astype(float)
#firData=np.insert(firData,0,firData[-1]) #ojo que pydfa me guarda 1 dato menos...
M = len(firData)

#--------------------------------------
def noise(n):
    return np.random.normal(0,0.2,n)

def x(n):
#    return 1*sc.sawtooth(2*np.pi*2*n,0.5)
#    return np.sin(2*np.pi*signalFrec1*n)+noise(len(n))
    return np.sin(2*np.pi*signalFrec1*n)+np.sin(2*np.pi*signalFrec2*n)


#------ x --------------------------------
xNData    = np.arange(0,N,1)
xTData    = xNData/fs
xData     = x(xTData)
signalAxe = fig.add_subplot(3,2,1)
signalAxe.set_title("Output side conv",rotation=0,fontsize=10,va="center")
signalLn,  = plt.plot(xTData,xData,'b-o',label="x",linewidth=3,alpha=0.3)
signalAxe.legend()
signalAxe.grid(True)
signalAxe.set_xlim(0,N/fs)

#------ h --------------------------------
hNData = np.arange(0,M,1)
hTData = hNData/fs
firAxe = fig.add_subplot(3,2,3)
firAxe.set_title(kernel,rotation=0,fontsize=10,va="center")
firLn, = plt.plot(hTData,firData,'g-o',label="h",linewidth=3,alpha=0.3)
firAxe.legend()
firAxe.grid(True)
firAxe.set_xlim(0,M/fs)

#------ conv --------------------------------
convAxe         = fig.add_subplot(3,2,5)
convolveData    = xData
for i in range(convStages):
    convolveData    = np.convolve(convolveData,firData)
    print(len(convolveData),len(firData))

convolveNData = np.arange(0,len(convolveData),1)
convolveTData = convolveNData/fs
convLn,       = plt.plot(convolveTData,convolveData,'r-',label = "numpy",linewidth = 6,alpha = 0.5)
convAxe.legend()
convAxe.grid(True)
convAxe.set_xlim(0,convolveTData[-1])

#------ X --------------------------------
XAxe          = fig.add_subplot(3,2,2)
XAxe.set_title("IDFT (DFT(x) x DFT(h))",rotation=0,fontsize=10,va="center")
XData         = np.fft.fft(xData)/N
circularXData = np.fft.fftshift(XData)
XFData        = xNData*(fs/(N-N%2))-fs/2
XLn,          = plt.plot(XFData,np.abs(circularXData)**2,'b-',label = "X",linewidth = 3,alpha = 0.5)
XAxe.legend()
XAxe.grid(True)
XAxe.set_xlim(-fs/2,fs/2-fs/N)

#------ H --------------------------------
HAxe          = fig.add_subplot(3,2,4)
HData         = np.fft.fft(firData)
circularHData = np.fft.fftshift(HData)
HFData        = hNData*(fs/(M-M%2))-fs/2
HLn,          = plt.plot(HFData,np.abs(circularHData),'g-',label = "H",linewidth = 3,alpha = 0.5)
HAxe.legend()
HAxe.grid(True)
HAxe.set_xlim(-fs/2,fs/2-fs/N)

#------ CONV --------------------------------
convN         = len(convolveData)
YAxe          = fig.add_subplot(3,2,6)
fData         = convolveNData*(fs/(convN-convN%2))-fs/2
YData         = np.fft.fft(convolveData)
circularYData = np.fft.fftshift(YData)
YLn,          = plt.plot(fData,np.abs(circularYData),'r-',label = "Y",linewidth = 3,alpha = 0.8)
YAxe.legend()
YAxe.grid(True)
YAxe.set_xlim(-fs/2,fs/2-fs/N)

plt.get_current_fig_manager().window.showMaximized()
plt.show()

