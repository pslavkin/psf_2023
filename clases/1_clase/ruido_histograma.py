import numpy as np
import scipy.signal as sc
import matplotlib.pyplot as plt

signalFrec = 1
N          = 1000
fs         = 1000
Bits       = 2
t          = np.arange(0,N/fs,1/fs)
signalC    = np.array([
             (2**7-1)*np.sin(2*np.pi*signalFrec*t)
             ,(2**7-1)*sc.sawtooth(2*np.pi*t,1)
             ,(2**7-1)*np.random.normal(0,1,len(t))
             ,120.5*sc.square(2*np.pi*t,0.5)
             ] ,dtype=np.float32).clip(-128,127)

signalQ  = np.copy(signalC).astype(np.int8)
signalQ  >>= 8-Bits
signalC  /= 2**(8-Bits)


fig = plt.figure()
for i in range(len(signalC)):
    contiAxe = fig.add_subplot(4,2,2*i+1)
    plt.step(t,signalC[i]-signalQ[i],'r-')
    contiAxe = fig.add_subplot(4,2,2*i+2)
    plt.hist((signalC[i]-signalQ[i]))

#mng=plt.get_current_fig_manager()
#mng.resize(*mng.window.maxsize())
plt.get_current_fig_manager().window.showMaximized() #para QT5
plt.show()
