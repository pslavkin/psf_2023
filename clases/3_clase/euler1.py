import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig        = plt.figure()
fs         = 20
N          = 200

circleAxe  = fig.add_subplot(1,2,1)
circleLn,  = plt.plot([],[],'ro',linewidth          = 5)
radioLn,   = plt.plot([0,0],[0.5,0.5],'g-',linewidth = 10,alpha = 0.2)
circleData = []
circleAxe.grid(True)
circleAxe.set_xlim(-1,1)
circleAxe.set_ylim(-1,1)
circleFrec = 1

nData=np.arange(0,N,1)

circle3DAxe = fig.add_subplot(1,2,2,projection = "3d")
circle3DLn,  = circle3DAxe.plot3D([], [], [])

def circle(f,n):
    #    return 1.4**(-1j*2*np.pi*f*n*1/fs) #what if e is not e??
    return np.exp(-1j*2*np.pi*f*n*1/fs)

def init():
    global circle3DLn,circleData
    circleData = []
    return circleLn,radioLn,circle3DLn

def update(n):
    global circle3DLn,circleData
    circleData.append(circle(circleFrec,n))
    circleLn.set_data(np.real(circleData),np.imag(circleData))
    radioLn.set_data([0,np.real(circle(circleFrec,n))],[0,np.imag(circle(circleFrec,n))])
    circle3DAxe.clear()
    circle3DLn = circle3DAxe.plot3D(np.real(circleData),np.imag(circleData),nData[:n+1],'g-o',linewidth=2)
    return circleLn,radioLn,circle3DLn

ani=FuncAnimation(fig,update,N,init,interval=100 ,blit=False,repeat=True)
plt.get_current_fig_manager().window.showMaximized() #para QT5
plt.show()
