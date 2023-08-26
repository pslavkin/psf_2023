import numpy as np
import scipy.signal as sc
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig        = plt.figure()
N          = 40
fig.suptitle('Ventanas para mejorar el efecto Gibbs N: {}'.format(N), fontsize=16)
#--------------------------------------
nData      = np.arange(0,N,1) #arranco con numeros enteros para evitar errores de float

#----------BLACKMAN----------------------------
winData=np.blackman(N)
winAxe = fig.add_subplot(3,1,1)
winAxe.set_title("Blackman",rotation=0,fontsize=10,va="center")
winLn, = plt.plot(nData,winData,'b-o',linewidth=4,alpha=0.2,label="data")
winAxe.grid(True)
#----------HAMMINGj----------------------------
winData=np.hamming(N) 
winAxe = fig.add_subplot(3,1,2)
winAxe.set_title("Hamming",rotation=0,fontsize=10,va="center")
winLn, = plt.plot(nData,winData,'r-o',linewidth=4,alpha=0.2,label="data")
winAxe.grid(True)
#----------GAUSS----------------------------
winData=sc.gaussian(N,20)
winAxe = fig.add_subplot(3,1,3)
winAxe.set_title("Gaussian",rotation=0,fontsize=10,va="center")
winLn, = plt.plot(nData,winData,'g-o',linewidth=4,alpha=0.2,label="data")
winAxe.grid(True)
###--------------------------------------
plt.get_current_fig_manager().window.showMaximized()
plt.show()
