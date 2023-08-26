import numpy as np
import scipy.signal as sc
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig        = plt.figure()
fig.suptitle('Efecto Gibbs al recortar la sinc', fontsize=16)
fs         = 100
N          = 1000
M          = 90
cutFrec    = 5
#--------------------------------------
nData      = np.arange(0,N,1) #arranco con numeros enteros para evitar errores de float
fData      = nData*(fs/((N)-(N)%2))-fs/2
tData      = nData/fs

#------------Escpectro--------------------------
fftData =  np.zeros(N).astype("complex")
for i in range(len(fData)):
    fftData[i]=0 if np.abs(fData[i])>cutFrec else 1

fftAxe  = fig.add_subplot(2,2,1)
fftAxe.set_title("Potencia calculada en frec: {0:.2f}".format(np.sum(np.abs(fftData)**2)/N),rotation=0,fontsize=10,va="center")
fftRLn, = plt.plot(fData,np.real(fftData),'b-o',linewidth=4,alpha=0.5,label="real")
fftILn, = plt.plot(fData,np.imag(fftData),'r-o',linewidth=4,alpha=0.2,label="imag")
fftAxe.grid(True)
##------------IFFT-----------------------
fftDataShifted = np.fft.fftshift(fftData)
ifftData       = np.fft.ifft(fftDataShifted)
ifftDataShifted= np.fft.fftshift(ifftData)
ifftDataShifted= ifftDataShifted[N//2-M//2:N//2+M//2]
#nData      = np.arange(0,N+M-1,1) #arranco con numeros enteros para evitar errores de float
#tData      = nData/fs
ifftDataShifted = np.concatenate((ifftDataShifted,np.zeros(N-M)))

ifftAxe = fig.add_subplot(2,1,2)
ifftAxe.set_title("Potencia calculada en Tiempo: {0:.2f}".format(np.sum(np.abs(ifftData)**2)),rotation=0,fontsize=10,va="center")
ifftRLn, = plt.plot(tData,np.real(ifftDataShifted),'b-o' ,linewidth  = 5,alpha = 0.5,label="Signal real")
ifftILn, = plt.plot(tData,np.imag(ifftDataShifted),'r-o' ,linewidth  = 5,alpha = 0.2,label="Signal imag")
fftAxe.grid(True)

#----------BLACKMAN----------------------------

windowData=np.blackman(N)

#----------FFT----------------------------
fftData        = np.fft.fft(ifftDataShifted)
fftDataShifted = np.fft.fftshift(fftData)

fftAxe       = fig.add_subplot(2,2,2)
fftAxe.set_title("Potencia calculada en fft: {0:.2f}".format(np.sum(np.abs(fftData)**2)/N),rotation=0,fontsize=10,va="center")
penAbsLn, = plt.plot(fData,np.abs(fftDataShifted)**2,'b-o',linewidth=4,alpha=0.5,label="Abs")
#penRLn, = plt.plot(fData,np.real(fftDataShifted),'b-o',linewidth=4,alpha=0.5,label="real")
#penILn  = plt.plot(fData,np.imag(fftDataShifted),'r-o',linewidth=4,alpha=0.2,label="imag")
fftAxe.grid(True)
###--------------------------------------
plt.get_current_fig_manager().window.showMaximized()
plt.show()
