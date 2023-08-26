import numpy as np
import scipy.signal as sc
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig        = plt.figure(1)
fig.suptitle('Zona de datos validad luego de una convolucion', fontsize=16)
def h():
#    return np.random.normal(0,2,128)
#    return np.array([0,1,2,3,4,5,4,3,2,1,0])
    return np.load("../utils/low_pass.npy").astype(float)[0]

N     = 100
fs    = 100
M     = len(h())
nData = np.arange(-(M-1),N+M-1,1) #agrega los M-1 pero tambien otross M-1 para calcular el y[0]
    
signalFrec1 = 2
signalFrec2 = 20

def x():
#    return [3,4,2]
    n = np.arange(0,N,1)/fs #agrega los M-1 pero tambien otross M-1 para calcular el y[0]
    return np.sin(2*np.pi*signalFrec1*n)+np.sin(2*np.pi*signalFrec2*n)
#    return np.random.normal(0,0.1,len(n))

#--------------------------------------

tData = nData/fs
xData = np.append(np.append(np.zeros(M-1),x()),np.zeros(M-1))
xAxe  = fig.add_subplot(3,1,1)
xLn,  = plt.plot(nData,xData,'r-o',label="xLen: {}".format(N),linewidth = 15,alpha = 0.2)
xZoneLn = xAxe.fill_between([0,0],100,-100,facecolor="yellow",alpha=0.5)
xAxe.legend()
xAxe.grid(True)
xAxe.set_xlim(-(M-1)-0.1,M+N-2+0.1)
xAxe.set_ylim(min(xData)-0.1,max(xData)+0.1)
xAxe.set_ylabel("señal",rotation=0,labelpad=20,fontsize=10,va="center")
#--------------------------------------

hDataFlip=np.flip(h(),0)
hAxe  = fig.add_subplot(3,1,2)
hLn,  = plt.plot([],[],'b-o',label="hLen: {}".format(M),linewidth = 15,alpha = 0.2)
hAxe.legend()
hAxe.grid(True)
hAxe.set_xlim(-(M-1)-0.1,M+N-2+0.1)
hAxe.set_ylim(min(hDataFlip)-0.4,max(hDataFlip)+0.4)
hAxe.set_ylabel("respuesta\n al impulso\n(flip)",rotation=0,labelpad=20,fontsize=8,va="center")
#--------------------------------------
yData   = np.zeros(N+M-1)
yAxe    = fig.add_subplot(3,1,3)
yLn,    = plt.plot([],[],'g-o',label="yLen: {}".format(len(yData)), linewidth = 15,alpha = 0.2)
yDotLn, = plt.plot([],[],'ko' ,label="valid [{}:{}]".format((N+M-1)/2-N/2,(N+M-1)/2+N/2), linewidth = 15,alpha = 0.8)
yAxe.legend()
yAxe.grid(True)
yAxe.set_xlim(-(M-1)-0.1,M+N-2+0.1)
yAxe.set_ylim(-2,2)
yAxe.set_ylabel("convolucion",rotation=0,labelpad=20,fontsize=8,va="center")
yZoneLn = yAxe.fill_between([(M-1)//2,(M-1)//2+N],100,-100,facecolor="yellow",alpha=0.5)
#--------------------------------------
def init():
    global yData
    yData *= 0
    return xLn,hLn,yLn,xZoneLn,yDotLn

def update(i):
    global hData,yData
    #input("actual loop: {}\r\n".format(i))
    hLn.set_data(nData[i:i+M],hDataFlip)

    yData[i]=np.sum(xData[i:i+M]*hDataFlip) #aca esta la operacion de convolucion punto a punto
    yLn.set_data(nData[M-1:M-1+M+N-1],yData)
    yDotLn.set_data(i,yData[i])
    xZoneLn = xAxe.fill_between([i-(M-1),i],100,-100,facecolor="yellow",alpha=0.5)

    return xLn,hLn,yLn,xZoneLn,yDotLn

ani=FuncAnimation(fig,update,N+M-1,init,interval=100 ,blit=True,repeat=False)
plt.get_current_fig_manager().window.showMaximized()
plt.show()
