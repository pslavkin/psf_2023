import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sc
#--------------------------------------
fig        = plt.figure()
fig.suptitle('Conversion desde pyfdax a include files en C', fontsize=16)
fs         = 10000
N          = 1027 #este se calcula como el largo de la FFT elegida MENOS M+1

#filterFile="low_pass.npy"
#filterFile="./filtro_band_stop_700.npy"
#filterFile="./pasa_bajos_500_clase6.npy"
#filterFile="../utils/band_pass_2_5_fs_10000.npy"
#filterFile="../utils/low_pass_2_fs10000.npy"
#filterFile="./band_pass_3k_fs10000.npy"
filterFile="band_pass_65_400.npy"
#filterFile="pasabajo_300.npy"
#filterFile="low_pass_600.npy"
#filterFile="low_pass_1500.npy"
#filterFile="filtro_500_blackman.npy"

#firData=np.transpose(np.load(filterFile).astype(float))[0]
firData=np.load(filterFile).astype(float)[0]
#firData=np.insert(firData,0,firData[-1]) #ojo que pydfa me guarda 1 dato menos...
M          = len(firData)

firExtendedData=np.concatenate((firData,np.zeros(N-1)))
impar=((N+M-1)%2)
#--------------------------------------
nData=np.arange(0,N+M-1,1)
tData=nData/fs
fData=nData*(fs/(N+M-1))-fs/2
#--------------------------------------
firAxe  = fig.add_subplot(2,1,1)
firAxe.set_title('h (respuesta al impulso unitaria extendida con zeros N: {})'.format(len(tData)), fontsize=16)
firLn,  = plt.plot(tData,firExtendedData,'b-o',label="h")
firAxe.legend()
firAxe.grid(True)
firAxe.set_xlim(0,(N+M-2)/fs)
firAxe.set_ylim(np.min(firData),np.max(firData))
#--------------------------------------
HData         = np.fft.fft(firExtendedData)
circularHData = np.abs(np.fft.fftshift(HData/M))**2
HAxe          = fig.add_subplot(2,1,2)
HAxe.set_title('H (DFT de la respuesta al impulso N: {})'.format(len(fData)), fontsize=16)
HLn,          = plt.plot(fData,circularHData,'r-o',label = "H")
HAxe.legend()
HAxe.grid(True)
HAxe.set_xlim(-fs/2,fs/2)
#--------------------------------------
def convertToC(h,H,fileName):
    cFile  = open(fileName,"w+")
    cFile.write("#define h_LENGTH {}\n".format(len(firData)))
    cFile.write("#define h_PADD_LENGTH {}\n".format(len(h)))
    cFile.write("#define H_PADD_LENGTH {}\n".format(len(H)))
    h*=2**15
    h=h.astype(np.int16)
    H*=2**15
    cFile.write("q15_t h[]={\n")
    for i in h:
        cFile.write("{},\n".format(i))
    cFile.write("};\n")
    cFile.write("q15_t H[]={\n")
    for i in H:
        cFile.write("{},{},\n".format(np.real(i).astype(np.int16),np.imag(i).astype(np.int16)))
    cFile.write("};\n")

    cFile.write("q15_t HAbs[]={\n")
    HAbs=np.abs(H)**2
    HAbs/=2**17
    for i in HAbs:
        cFile.write("{},\n".format(i.astype(np.int16)))
    cFile.write("};\n")

convertToC(firExtendedData,HData,"fir.h")
plt.get_current_fig_manager().window.showMaximized()
plt.show()
