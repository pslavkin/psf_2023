import numpy as np
import scipy.signal as sc
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig   = plt.figure(1)
fs    = 20
N     = 60
signalFrec = 1
nSequence = np.arange(0,N,1)

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
impulseAxe.set_ylabel("descomposicion\n en impulsos",rotation=0,labelpad=20,fontsize=8,va="center")
#--------------------------------------
accumAxe  = fig.add_subplot(3,1,3)
accumLn1, = plt.plot([],[],'r-o',linewidth = 15,alpha = 0.2)
accumLn2, = plt.plot([],[],'b-o',linewidth = 15,alpha = 0.2)
accumAxe.grid(True)
accumAxe.set_xlim(0,tData[-1])
accumAxe.set_ylim(-2.2,2.2)
accumAxe.set_ylabel("superposicion",rotation=0,labelpad=20,fontsize=8,va="center")
#--------------------------------------
def init():
    global signalData,impulseData
    signalData=[]
    impulseData=[]
    return signalLn,impulseLn,accumLn1,accumLn2

def update(i):
    global signalData,impulseData
    #input()
    signalData.append(signal(i))
    signalLn.set_data(tData[:i+1],signalData)

    impulseData=signalData[-1]*impulse(N,i)
    impulseLn.set_data(tData,impulseData)

    accumLn1.set_data(tData[:i+1],signalData)
    accumLn2.set_data(tData,impulseData)
    return signalLn,impulseLn,accumLn1,accumLn2

ani=FuncAnimation(fig,update,N,init,interval=100 ,blit=False,repeat=True)
plt.get_current_fig_manager().window.showMaximized()
plt.show()
