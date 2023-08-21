import numpy as np
import scipy.signal as sc
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig        = plt.figure()
fig.suptitle('Signal <> DFT < Espectro > IDFT <> Signal y potencia con Numpy', fontsize=16)
fs         = 1000
N          = 1000
signalFrec = 1
#--------------------------------------
nData      = np.arange(0,N,1) #arranco con numeros enteros para evitar errores de float
tData      = nData/fs
fData      = nData*(fs/((N)-(N)%2))-fs/2

#------------SIGNAL--------------------------
#signalData = 1*np.cos(2*np.pi*signalFrec*nData*1/fs)
#signalData = 1*np.sin(2*np.pi*signalFrec*nData*1/fs)+0.4j*np.sin(2*np.pi*signalFrec*nData*1/fs)
#signalData = 1*np.sin(2*np.pi*signalFrec*nData*1/fs)
signalData = 2*sc.square(2*np.pi*signalFrec*nData*1/fs,0.5)
#signalData = 2*sc.sawtooth(2*np.pi*signalFrec*nData*1/fs,1)
#signalData = np.array([100 if n == 10 else 0 for n in nData])


signalAxe  = fig.add_subplot(2,2,1)
signalAxe.set_title("Potencia calculada en tiempo: {0:.2f}".format(np.sum(np.abs(signalData)**2)/N),rotation=0,fontsize=10,va="center")
signalRLn, = plt.plot(tData,np.real(signalData),'b-o',linewidth=4,alpha=0.5,label="real")
signalILn, = plt.plot(tData,np.imag(signalData),'r-o',linewidth=4,alpha=0.5,label="imag")
signalAxe.grid(True)
#------------FFT IFFT-----------------------
fftData  = np.fft.fft(signalData)
ifftData = np.fft.ifft(fftData)
fftData  = np.fft.fftshift(fftData)
#-----------FFT---------------------------
fftAxe                 = fig.add_subplot(2,1,2)
fftAxe.set_title("Potencia calculada en frec: {0:.2f}".format(np.sum(np.abs(fftData/N)**2)),rotation=0,fontsize=10,va="center")
fftAbsLn, = plt.plot(fData,np.abs(fftData/N)**2,'k-X' ,linewidth  = 5,alpha = 0.3,label="Potencia")
#fftRLn,   = plt.plot(fData,np.real(fftData),   'b-X' ,linewidth = 4,alpha  = 0.5,label="real")
#fftILn,   = plt.plot(fData,np.imag(fftData),   'r-X' ,linewidth = 4,alpha  = 0.5,label="imag")
fftAxe.grid(True)
#----------IFFT----------------------------
ifftAxe       = fig.add_subplot(2,2,2)
ifftAxe.set_title("Potencia calculada en ifft: {0:.2f}".format(np.sum(np.abs(ifftData)**2)/N),rotation=0,fontsize=10,va="center")
penRLn, = plt.plot(tData,np.real(ifftData),'b-o',linewidth=4,alpha=0.5,label="real")
penILn  = plt.plot(tData,np.imag(ifftData),'r-o',linewidth=4,alpha=0.5,label="imag")
ifftAxe.grid(True)
#--------------------------------------
plt.get_current_fig_manager().window.showMaximized()
plt.show()
