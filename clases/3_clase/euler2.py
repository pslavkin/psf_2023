import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig        = plt.figure()
fs         = 20
N          = 20
#--------------------------------------
circleAxe  = fig.add_subplot(2,2,1)
circleLn , = plt.plot([] ,[] ,'ro-' ,linewidth = 5)
radioLn,  = plt.plot([0,0],[0.5,0.5],'g-',linewidth = 10,alpha = 0.2)
circleAxe.grid(True)
circleAxe.set_xlim(-1,1)
circleAxe.set_ylim(-1,1)
circleLn.set_label(0)
circleLg=circleAxe.legend()
circleFrec = 1
circleData = []
def circle(f,n):
    return np.exp(-1j*2*np.pi*f*n*1/fs)
#--------------------------------------
signalAxe = fig.add_subplot(2,2,2)
signalLn, = plt.plot([],[],'b-o')
signalAxe.grid(True)
signalAxe.set_xlim(0,N/fs)
signalAxe.set_ylim(-1,1)
signalFrec = 3
signalData=[]
def signal(f,n):
    return np.cos(2*np.pi*f*n*1/fs)
#--------------------------------------
tData=np.arange(0,N,1)/fs

def init():
    global circleData,signalData
    circleData=[]
    signalData=[]
    return circleLn,circleLg,signalLn,radioLn,

def update(n):
    global circleData,signalData,radioLn
    circleData.append(circle(circleFrec,n))
    circleLn.set_data(np.real(circleData), np.imag(circleData))

    signalData.append(signal(signalFrec,n))
    signalLn.set_data(tData[:n+1],signalData)

    radioLn.set_data([0,np.real(circleData[-1])],[0,np.imag(circleData[-1])])

    circleLn.set_label(n)
    circleLg=circleAxe.legend()
    return circleLn,circleLg,signalLn,radioLn,

ani=FuncAnimation(fig,update,N,init,interval=50 ,blit=False,repeat=True)
plt.get_current_fig_manager().window.showMaximized()
plt.show()
