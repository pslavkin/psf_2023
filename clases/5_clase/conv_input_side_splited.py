import numpy as np
import scipy.signal as sc
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig   = plt.figure(1)
fig.suptitle('Convolucion input side - splited', fontsize=16)
fs    = 1
N     = 2
M     = 2
xFrec = 1/5
nData = np.arange(0,N+M-1,1)
#--------------------------------------
def x(n):
    return np.array([3,4])[n]
#    return 1*sc.sawtooth(2*np.pi*xFrec*n/fs,0.1)
#    return 1*np.sin(2*np.pi*xFrec*n/fs)

tData = nData/fs
xData = []
xAxe  = fig.add_subplot(2+N,1,1)
xLn,  = plt.plot([],[],'r-o',linewidth = 15,alpha = 0.2)
xAxe.grid(True)
xAxe.set_xlim(0,tData[-1])
xAxe.set_ylim(0,10)
xAxe.set_ylabel("señal",rotation=0,labelpad=20,fontsize=10,va="center")
#--------------------------------------
def h():
    return np.array([1,2])
#ans=np.zeros(M)
#    ans[0]=1
#    ans[1]=-1
#    return ans

hData = []
hAxe  = []
hLn   = []
for i in range(N):
    hAxe.append(fig.add_subplot(2+N,1,2+i))
    hLn.append(plt.plot([],[],'b-o',linewidth = 15,alpha = 0.2)[0])
    hAxe[-1].grid(True)
    hAxe[-1].set_xlim(0,tData[-1])
    hAxe[-1].set_ylim(0,10)
    hAxe[-1].set_ylabel("respuesta\n al impulso: {}".format(i),rotation=0,labelpad=20,fontsize=8,va="center")
#--------------------------------------
yData = np.zeros(N+M-1)
yAxe  = fig.add_subplot(2+N,1,2+N)
yLn,  = plt.plot([],[],'g-o',linewidth = 15,alpha = 0.2)
yAxe.grid(True)
yAxe.set_xlim(0,tData[-1])
yAxe.set_ylim(0,10)
yAxe.set_ylabel("convolucion",rotation=0,labelpad=20,fontsize=8,va="center")
#--------------------------------------
def init():
    global xData,hData,yData
    xData  = []
    hData  = []
    yData *= 0
    for i in range(N):
        hLn[i].set_data([],[])
    return xLn,hLn[0],yLn

def update(i):
    global xData,hData,yData
    input()
    xData.append(x(i))
    xLn.set_data(tData[:i+1],xData)

    hData=xData[-1]*h()
    hLn[i].set_data(tData[i:i+M],hData)

    yData[i:i+M]+=hData
    yLn.set_data(tData,yData)

    return xLn,hLn[i],yLn

ani=FuncAnimation(fig,update,N,init,interval=1000 ,blit=False,repeat=True)
plt.get_current_fig_manager().window.showMaximized()
plt.show()
