import numpy as np
import scipy.signal as sc
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig        = plt.figure(1)
fig.suptitle('Input side convolution', fontsize=16)
fs    = 3
N     = 2
M     = 2
xFrec = 1
nData = np.arange(0,N+M-1,1)

#--------------------------------------
def x(n):
    return np.array([3,4])[n]

tData = nData/fs
xData = []
xAxe  = fig.add_subplot(3,1,1)
xLn,  = plt.plot([],[],'r-o',linewidth = 15,alpha = 0.2)
xAxe.grid(True)
xAxe.set_xlim(-0.1,M+N-1-0.9)
xAxe.set_ylim(0,5)
xAxe.set_ylabel("señal",rotation=0,labelpad=20,fontsize=10,va="center")
#--------------------------------------
def h():
    return np.array([1,2])

hData = []
hAxe  = fig.add_subplot(3,1,2)
hLn,  = plt.plot([],[],'b-o',linewidth = 15,alpha = 0.2)
hAxe.grid(True)
hAxe.set_xlim(-0.1,M+N-1-0.9)
hAxe.set_ylim(0,3)
hAxe.set_ylabel("respuesta\n al impulso",rotation=0,labelpad=20,fontsize=8,va="center")
#--------------------------------------
yData = np.zeros(N+M-1)
yAxe  = fig.add_subplot(3,1,3)
yLn,  = plt.plot([],[],'g-o',linewidth = 15,alpha = 0.2)
yAxe.grid(True)
yAxe.set_xlim(-0.1,M+N-1-0.9)
yAxe.set_ylim(0,12)
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
    #input("actual loop: {}\r\n".format(i))

    xData.append(x(i))
    xLn.set_data(nData[:i+1],xData)

    hData=h()
    hLn.set_data(nData[i:i+M],hData)

    yData[i:i+M]+=xData[-1]*hData
    yLn.set_data(nData,yData)

    return xLn,hLn,yLn

ani=FuncAnimation(fig,update,N,init,interval=100 ,blit=False,repeat=True)
plt.get_current_fig_manager().window.showMaximized()
plt.show()
