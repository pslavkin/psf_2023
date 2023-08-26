import numpy as np
import scipy.signal as sc
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig   = plt.figure(1)
fig.suptitle('Convolucion', fontsize=16)
fs    = 20
N     = 60
M     = 5
xFrec = 1
nData = np.arange(0,N+M-1,1)

#--------------------------------------
def x(n):
    return 2*sc.sawtooth(2*np.pi*xFrec*n/fs,0.5)
    return 2*np.sin(2*np.pi*xFrec*n/fs)

tData = nData/fs
xData = []
xAxe  = fig.add_subplot(3,1,1)
xLn,  = plt.plot([],[],'r-o',linewidth = 15,alpha = 0.2)
xAxe.grid(True)
xAxe.set_xlim(0,tData[-1])
xAxe.set_ylim(-2,2)
xAxe.set_ylabel("señal",rotation=0,labelpad=20,fontsize=10,va="center")
#--------------------------------------
def h():
    ans=np.zeros(M)
    ans[0]=1
    ans[1]=-1
    return ans

hData = []
hAxe  = fig.add_subplot(3,1,2)
hLn,  = plt.plot([],[],'b-o',linewidth = 15,alpha = 0.2)
hAxe.grid(True)
hAxe.set_xlim(0,tData[-1])
hAxe.set_ylim(-2.2,2.2)
hAxe.set_ylabel("respuesta\n al impulso",rotation=0,labelpad=20,fontsize=8,va="center")
#--------------------------------------
yData = np.zeros(N+M-1)
yAxe  = fig.add_subplot(3,1,3)
yLn,  = plt.plot([],[],'g-o',linewidth = 15,alpha = 0.2)
yAxe.grid(True)
yAxe.set_xlim(0,tData[-1])
yAxe.set_ylim(-2.2,2.2)
yAxe.set_ylabel("convolucion",rotation=0,labelpad=20,fontsize=8,va="center")
#--------------------------------------
def init():
    global xData,hData,yData
    xData  = []
    hData  = []
    yData *= 0
    return xLn,hLn,yLn

def update(i):
    global xData,hData,yData
    xData.append(x(i))
    xLn.set_data(tData[:i+1],xData)

    hData=xData[-1]*h()
    hLn.set_data(tData[i:i+M],hData)

    yData[i:i+M]+=hData
    yLn.set_data(tData,yData)

    return xLn,hLn,yLn

ani=FuncAnimation(fig,update,N,init,interval=100 ,blit=False,repeat=True)
plt.get_current_fig_manager().window.showMaximized()
plt.show()
