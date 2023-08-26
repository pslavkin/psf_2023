import numpy as np
import scipy.signal as sc
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig        = plt.figure()
fs         = 100
N          = 500
M          = 200
cutFrec    = 2
fig.suptitle('Efecto Gibbs al recortar la sinc fs: {} N: {} M: {}'.format(fs,N,M), fontsize=16)
#--------------------------------------
nData      = np.arange(0,N,1) #arranco con numeros enteros para evitar errores de float
fData      = nData*(fs/(N-N%2))-fs/2
tData      = nData/fs

#------------Escpectro--------------------------
fftData =  np.zeros(N).astype("complex")
for i in range(len(fData)):
    fftData[i]=0 if np.abs(fData[i])>cutFrec else 1

spectreAxe  = fig.add_subplot(3,2,1)
spectreAxe.set_title("Plantilla de filtro en frecuencia ideal N: {}".format(len(fData)),rotation=0,fontsize=10,va="center")
fftRLn, = plt.plot(fData,np.real(fftData),'b-',linewidth=2,alpha=0.5,label="Plantilla ideal")
#fftILn, = plt.plot(fData,np.imag(fftData),'r-',linewidth=2,alpha=0.2,label="imag")
spectreAxe.grid(True)
spectreAxe.legend()
#----------BLACKMAN----------------------------

#winData=np.blackman(M)
#winData=np.hamming(M) 
winData=sc.gaussian(M,20)

winAxe       = fig.add_subplot(3,1,3)
winAxe.set_title("Window con M: {}".format(M),rotation=0,fontsize=10,va="center")
winLn, = plt.plot(nData[:M],winData,'b-',linewidth=2,alpha=0.5,label="Window")
winAxe.grid(True)
winAxe.legend()
##------------SIGNAL IFFT-----------------------
fftDataShifted = np.fft.fftshift(fftData)
ifftData       = np.fft.ifft(fftDataShifted)
ifftDataShifted= np.fft.fftshift(ifftData)
ifftDataShifted= ifftDataShifted[N//2-M//2:N//2+M//2]

#------aplico ventaneo ----------------------
ifftDataShiftedW=ifftDataShifted*winData
#descomentar la siguiente linea para aplicar la ventana
ifftDataShifted=ifftDataShiftedW

ifftDataShiftedW = np.concatenate((ifftDataShiftedW,np.zeros(N-M)))
ifftDataShifted = np.concatenate((ifftDataShifted,np.zeros(N-M)))

ifftAxe = fig.add_subplot(3,1,2)
ifftAxe.set_title("Antitransformada de la respuesta al impulso M: {}, padding: {} N: {}".format(M,N-M,N),rotation=0,fontsize=10,va="center")
ifftRLn, = plt.plot(tData,np.real(ifftDataShifted),'b-' ,linewidth  = 2,alpha = 0.5,label="Signal real")
ifftRWindowedLn, = plt.plot(tData,np.real(ifftDataShiftedW),'g-' ,linewidth  = 2,alpha = 0.5,label="Signal real windowed")
#ifftILn, = plt.plot(tData,np.imag(ifftDataShifted),'r-' ,linewidth  = 2,alpha = 0.2,label="Signal imag")
ifftAxe.legend()
ifftAxe.grid(True)


#----------FFT----------------------------
fftData        = np.fft.fft(ifftDataShifted)
fftDataShifted = np.fft.fftshift(fftData)

fftAxe       = fig.add_subplot(3,2,2)
fftAxe.set_title("Transformada de respuesta al impulso real",rotation=0,fontsize=10,va="center")
penAbsLn, = plt.plot(fData,np.abs(fftDataShifted)**2,'b-',linewidth=2,alpha=0.5,label="Abs")
#penRLn, = plt.plot(fData,np.real(fftDataShifted),'b-',linewidth=2,alpha=0.5,label="real")
#penILn  = plt.plot(fData,np.imag(fftDataShifted),'r-',linewidth=2,alpha=0.2,label="imag")
fftAxe.legend()
fftAxe.grid(True)
###--------------------------------------
plt.get_current_fig_manager().window.showMaximized()
plt.show()
