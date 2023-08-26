import numpy as np
import scipy.signal as sc
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig        = plt.figure(1)
fig.suptitle('Descomposicion de señal en deltas', fontsize=16)
fs         = 10
N          = 10
signalFrec = 1
nData      = np.arange(0,N,1)

#--------------------------------------
def signal():
    return 2*np.sin(2*np.pi*signalFrec*nData/fs)
    return [1,2,0,-2,-1]

tData      = nData/fs
signalAxe  = fig.add_subplot(6,1,1)
gridSpec   = signalAxe.get_gridspec()

signalLn,      = plt.plot(tData,signal(),'r-o',linewidth = 10,alpha = 0.4)
signalPointLn, = plt.plot([],[],'ko',linewidth           = 10,alpha = 0.8)
#signalAxe.grid(True)
signalAxe.set_xlim(0,tData[-1])
signalAxe.set_ylim(min(signal())-0.5,max(signal())+0.5)
signalAxe.set_ylabel("señal",rotation=0,labelpad=20,fontsize=10,va="center")
#--------------------------------------
def impulse(n,pos):
    ans=np.zeros(n)
    ans[pos]=1
    return ans

impulseAxe=fig.add_subplot(gridSpec[1:,0])
impulseAxe.set_ylabel("descomposicion\n en impulsos",rotation=0,labelpad=10,fontsize=8,va="center")
space=(np.abs(min(signal()))+np.abs(max(signal())))+1
impulsePointLn , = plt.plot ( [] ,[] ,'ko' ,linewidth = 10 ,alpha = 1 )
impulseAxe.grid(True)
impulseAxe.set_xlim(0,tData[-1])
impulseAxe.set_ylim(-N*space,max(signal())-0.2)
impulseZoneLn = impulseAxe.fill_between([0,0],100,-100,facecolor="yellow",alpha=0.5)

impulseLn=[]
for i in range(N):
    impulseLn.append(plt.plot([],[],'b-o',linewidth = 4,alpha = 0.4)[0])

#--------------------------------------
def init():
    global impulseLn
    for i in range(N):
        impulseLn[i].set_data([],[])
    impulsePointLn.set_data([],[])
    return impulseLn,signalPointLn,impulsePointLn,impulseZoneLn

def update(i):
    global impulseLn
    impulseData=signal()[i]*impulse(N,i)
    impulseLn[i].set_data(tData,impulseData-i*space)
    signalPointLn.set_data(tData[i],signal()[i])
    impulsePointLn.set_data(tData[i],(impulseData-i*space)[i])
    impulseZoneLn = impulseAxe.fill_between([tData[i]-1/(10*fs),tData[i]+1/(10*fs)],(impulseData-i*space)[i]+0.2*space,(impulseData-i*space)[i]-0.2*space,facecolor="yellow",alpha=0.5)
    return impulseLn,signalPointLn,impulsePointLn,impulseZoneLn

ani=FuncAnimation(fig,update,N,init,interval=2000 ,blit=False,repeat=True)
plt.get_current_fig_manager().window.showMaximized()
plt.show()
