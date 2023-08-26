import numpy as np
import scipy.signal as sc
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig        = plt.figure(1)
fs         = 20
N          = 60
M          = 10
signalFrec = 1
nSequence = np.arange(0,N+M-1,1)

#--------------------------------------
def signal(n):
    return 2*np.sin(2*np.pi*signalFrec*n/fs)

tData      = nSequence/fs
signalData = []
signalAxe  = fig.add_subplot(3,1,1)
signalLn,  = plt.plot([],[],'r-o',linewidth = 15,alpha = 0.2)
signalAxe.grid(True)
signalAxe.set_xlim(0,tData[-1])
signalAxe.set_ylim(-2.2,2.2)
signalAxe.set_ylabel("señal",rotation=0,labelpad=20,fontsize=10,va="center")
#--------------------------------------
def impulse(n,pos):
    ans=np.zeros(n)
    ans[pos]=1
    return ans

impulseData = []
impulseAxe  = fig.add_subplot(3,1,2)
impulseLn,  = plt.plot([],[],'b-o',linewidth = 15,alpha = 0.2)
impulseAxe.grid(True)
impulseAxe.set_xlim(0,tData[-1])
impulseAxe.set_ylim(-2.2,2.2)
impulseAxe.set_ylabel("impulsos",rotation=0,labelpad=20,fontsize=8,va="center")
#--------------------------------------
def impulseResponse():
    ans=np.zeros(M)
    ans[0]=1
    ans[1]=0.5
    ans[2]=-1
    return ans

impulseResponseData = []
impulseResponseAxe  = fig.add_subplot(3,1,3)
impulseResponseLn,  = plt.plot([],[],'g-o',linewidth = 15,alpha = 0.2)
impulseResponseAxe.grid(True)
impulseResponseAxe.set_xlim(0,tData[-1])
impulseResponseAxe.set_ylim(-2.2,2.2)
impulseResponseAxe.set_ylabel("respuesta\n al impulso",rotation=0,labelpad=20,fontsize=8,va="center")
#--------------------------------------
def init():
    global signalData,impulseData,impulseResponseData
    signalData          = []
    impulseData         = []
    impulseResponseData = []
    return signalLn,impulseLn,impulseResponseLn

def update(i):
    global signalData,impulseData,impulseResponseData
    #input()
    signalData.append(signal(i))
    signalLn.set_data(tData[:i+1],signalData)

    impulseData=signalData[-1]*impulse(N,i)
    impulseLn.set_data(tData[:N],impulseData)

    impulseResponseData=signalData[-1]*impulseResponse()
    impulseResponseLn.set_data(tData[i:i+M],impulseResponseData)

    return signalLn,impulseLn,impulseResponseLn

ani=FuncAnimation(fig,update,N,init,interval=100 ,blit=False,repeat=True)
plt.get_current_fig_manager().window.showMaximized()
plt.show()
