import numpy as np
import matplotlib.pyplot as plt

NC  = 100
fsC = 20
tCn = np.arange(-NC//2,NC//2,1)
tC  = tCn/fsC
f   = tCn * fsC/NC
B=3
sinc=np.sinc(2*B*(tC))

fig        = plt.figure()

contiAxe = fig.add_subplot(2,1,1)
plt.plot(tC,sinc,'b-',tC,tC*0,'r-')
plt.grid()

contiAxe = fig.add_subplot(2,1,2)
fftSinc=1/NC*np.abs(np.fft.fft(sinc)**2)
fftSinc=np.fft.fftshift(fftSinc)
plt.plot(f,fftSinc,'b-')
plt.grid()

plt.get_current_fig_manager().window.showMaximized() #para QT5
plt.show()
