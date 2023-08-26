import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig        = plt.figure()
fs         = 8.0
N          = 8
#--------------------------------------
circleAxe  = fig.add_subplot(2,2,1)
circleLn, = plt.plot([] ,[] ,'ro-' ,linewidth = 2)
massLn,   = plt.plot([] ,[] ,'bX' ,linewidth = 1 ,alpha = 1)

circleAxe.grid(True)
circleAxe.set_xlim(-1,1)
circleAxe.set_ylim(-1,1)

nData = np.arange(0,N,1) #arranco con numeros enteros para evitar errores de float
circleFrec = (nData-N//2)*fs/N
circleLn.set_label(circleFrec[0])
circleLg   = circleAxe.legend()
circleData = []
mass       = 0
frecIter   = -1
def circle(f,n):
    return np.exp(-1j*2*np.pi*f*n*1/fs)

circleFixedLn, = circleAxe.plot(np.real(circle(fs/N,nData)) ,np.imag(circle(fs/N,nData)) ,'go-' ,linewidth = 4,alpha=0.4)
#--------------------------------------
signalAxe  = fig.add_subplot(2,2,2)
signalLn,  = plt.plot([],[],'b-o')
signalRLn,  = plt.plot([],[],'b-o',linewidth=3,alpha=0.6)
signalILn,  = plt.plot([],[],'r-o',linewidth=3,alpha=0.6)
signalAxe.grid(True)
signalAxe.set_xlim(0,N/fs)
signalAxe.set_ylim(-2,2)
signalFrec = 2
signalData=[]
def signal(f,n):
    return 1*np.cos(2*np.pi*f*n*1/fs)#+0.5* np.cos(2*np.pi*3*n*1/fs)
#    if n<50: 
#     return 0.5*np.sin(2*np.pi*f*n*1/fs)+0.5*np.sin(2*np.pi*f*1.5*n*1/fs)
#    return 0
#--------------------------------------
promAxe  = fig.add_subplot(2,2,3)
promRLn,promILn,promMagLn,promPhaseLn  = plt.plot([],[],'b-o',[],[],'r-o',[],[],'k-',[],[],'y-')
promAxe.grid(True)
promAxe.set_xlim(-fs/2,fs/2)
promAxe.set_ylim(-1,1)
promData=np.zeros(N,dtype=complex)
#--------------------------------------
prom3DAxe = fig.add_subplot(2,2,4,projection = "3d")
def plot3DLn(x,y,z):
    prom3DAxe.clear()
    prom3DLn = prom3DAxe.plot3D(x,y,z,'g-o',linewidth=2)
    prom3DAxe.set_xlim(-fs/2,fs/2)
    prom3DAxe.set_ylim(-1,1)
    prom3DAxe.set_zlim(-1,1)

#--------------------------------------
tData=nData/fs

def init():
    global frecIter
    frecIter+=1
    if frecIter >= (N-1):
        ani.repeat=False
    return circleLn,circleLg,signalRLn,signalILn,massLn,promRLn,promILn

def update(nn):
    global circleData,signalData,promData,frecIter,circleFrec,circleLg
    circleData = []
    signalData = []
    powerAverage=0.0
    for n in range(N):
        circleData.append(circle(circleFrec[frecIter],n)*signal(signalFrec,n))
        mass=np.average(circleData)
        signalData.append(signal(signalFrec,n))
        promData[frecIter]=mass
    massLn.set_data(np.real(mass),
                    np.imag(mass))
    circleLn.set_data(np.real(circleData),
                      np.imag(circleData))
    signalRLn.set_data(tData[:n+1],np.real(signalData))
    signalILn.set_data(tData[:n+1],np.imag(signalData))
#    promRLn.set_data(circleFrec[:frecIter+1],np.real(promData[:frecIter+1]))
#    promILn.set_data(circleFrec[:frecIter+1],np.imag(promData[:frecIter+1]))
    promMagLn.set_data(circleFrec[:frecIter+1],np.abs(promData[:frecIter+1])**2)
#    promPhaseLn.set_data(circleFrec[:frecIter+1],np.angle(promData[:frecIter+1])/np.pi)
    circleLn.set_label(circleFrec[frecIter])
    circleLg=circleAxe.legend()

    plot3DLn(circleFrec[:frecIter+1],np.real(promData[:frecIter+1]),np.imag(promData[:frecIter+1]))

    return circleLn,circleLg,signalRLn,signalILn,massLn,promRLn,promILn,promMagLn,promPhaseLn,

ani=FuncAnimation(fig,update,1,init,interval=1 ,blit=False,repeat=True)
plt.get_current_fig_manager().window.showMaximized()
plt.show()
