import numpy                as     np
import matplotlib.pyplot    as     plt
from   matplotlib.animation import FuncAnimation
import scipy.signal         as     sc
#--------------------------------------
fig  = plt.figure(1)
fig.suptitle('Transformada inversa de Fourier', fontsize=16)
fs   = 20
N    = 20
skip = 0
#-------Diferentes señales de interes-------------------------------
def signal(f,n):
#    return 1*np.cos(2*np.pi*f*n*1/fs)
#    return 1j*np.cos(2*np.pi*f*n*1/fs)
#    return np.cos(2*np.pi*f*n*1/fs)+0.2j*np.cos(2*np.pi*2*f*n*1/fs)#+0.4j*np.cos(2*np.pi*2.5*f*n*1/fs)
#
#    return 0.5*sc.square  (2*np.pi*f*n*1/fs,0.5)
#    return 1*sc.sawtooth(2*np.pi*f*n*1/fs,1)
#    return 10 if n == 0 else 0
    return 10j if n == 1 else -10j if n==N-1 else 0
#    return 10 if n == N//2 else 0
#-----Cargo formas de onda desde archivos npy---------------------------
#conejo=np.load("../utils/pajaro.npy")[::1]
#conejo=np.load("../utils/conejo.npy")[::1]
#N=len(conejo)
#def signal(f,n):
#    return conejo[n]
#--------------------------------------
nData       = np.arange(0,N,1) #arranco con numeros enteros para evitar errores de float
#--------------------------------------
circleAxe  = fig.add_subplot(2,2,1)
circleAxe.set_title("señal x circulo",rotation=0,fontsize=10,va="center")
circleLn,massLn,  = plt.plot([],[],'r-',[],[],'bo')
circleAxe.grid(True)
circleAxe.set_xlim(-1,1)
circleAxe.set_ylim(-1,1)
circleFrec = (nData-N//2)*fs/N
circleLn.set_label(circleFrec[0])
circleLg   = circleAxe.legend()
circleData = []
mass       = 0
def circle(f,n):
    return   np.exp(-1j*2*np.pi*f*n*1/fs)

def circleInv(f,n,c):
    return c*np.exp( 1j*2*np.pi*f*n*1/fs)
#--------------------------------------
signalAxe  = fig.add_subplot(2,2,2)
signalAxe.set_title("señal",rotation=0,fontsize=10,va="center")
signalRLn,  = plt.plot([],[],'b-o',linewidth=3,alpha=0.6)
signalILn,  = plt.plot([],[],'r-o',linewidth=3,alpha=0.6)
signalAxe.grid(True)
signalAxe.set_xlim(0,(N-1)/fs)
signalAxe.set_ylim(-1,1)
signalFrec = 1
signalData=[]

#--------------------------------------
promAxe  = fig.add_subplot(2,2,3)
promAxe.set_title("Transformada DFT",rotation=0,fontsize=10,va="center")
promRLn,promILn,  = plt.plot([],[],'g-o',[],[],'y-o')
promAxe.grid(True)
promAxe.set_xlim(-fs/2-fs/N,fs/2+fs/N)
promAxe.set_ylim(-1,1)
promData=np.zeros(N,dtype=complex)
promZoneLn = promAxe.fill_between([circleFrec[skip//2],circleFrec[N-1-skip//2]],100,-100,facecolor="yellow",alpha=0.2)
#--------------------------------------
inversaAxe = fig.add_subplot(2,2,4)
inversaAxe.set_title("Antitransformada I-DFT",rotation=0,fontsize=10,va="center")
inversaAxe.set_ylabel("real",rotation=0,fontsize=10,va="center")
inversaAxe.set_xlabel("imag",rotation=0,fontsize=10,va="center")
inversaLn, = plt.plot([],[],'m-o')
penLn,     = plt.plot([],[],'k-o',linewidth=10,alpha=0.2)
penRLn,    = plt.plot([],[],'b-')
penILn,    = plt.plot([],[],'r-')
inversaAxe.grid(True)
inversaAxe.set_xlim(-1,1)
inversaAxe.set_ylim(-1,1)
penData= []
#--------------------------------------
tData       = nData/fs
signalsIter = 0

def init():
    return circleLn,circleLg,signalRLn,signalILn,massLn,promRLn,promILn,inversaLn

def updateF(frecIter):
    global promData,fData,penData
    inversaData=[0]
    #input()
    for f in range(N-skip):
        inversaData.append(inversaData[-1]+circleInv(circleFrec[f+skip//2],frecIter,promData[f+skip//2]))
    inversaLn.set_data(np.imag(inversaData),np.real(inversaData))
    penData.insert(0,inversaData[-1])
    penData=penData[0:N]
    t=np.linspace(0,-1,len(penData))
    penRLn.set_data(t,np.real(penData))
    penILn.set_data(np.imag(penData),t)
    penLn.set_data(np.imag(penData),np.real(penData))
    return circleLn,circleLg,signalRLn,signalILn,massLn,promRLn,promILn,promZoneLn

def updateT(frecIter):
    global circleData,signalData,promData,circleFrec,circleLg,signalsIter

    circleData = []
    signalData = []
    for n in range(N):
        circleData.append(circle(circleFrec[frecIter],n)*signal(signalFrec,n))
        mass=np.average(circleData)
        signalData.append(signal(signalFrec,n))
        promData[frecIter]=mass
        signalRLn.set_data(tData[:n+1],np.real(signalData))
        signalILn.set_data(tData[:n+1],np.imag(signalData))
    massLn.set_data(np.real(mass),
                    np.imag(mass))
    circleLn.set_data(np.real(circleData),
                      np.imag(circleData))
    promRLn.set_data(circleFrec[:frecIter+1],np.real(promData[:frecIter+1]))
    promILn.set_data(circleFrec[:frecIter+1],np.imag(promData[:frecIter+1]))
    circleLn.set_label(circleFrec[frecIter])
    circleLg=circleAxe.legend()
    if frecIter==N-1:
        aniT._func     = updateF
        aniT._interval = 100
        signalsiter=0

    return circleLn,circleLg,signalRLn,signalILn,massLn,promRLn,promILn,promZoneLn

aniT=FuncAnimation(fig,updateT,N,init,interval=10 ,blit=False,repeat=True,cache_frame_data=False)
plt.get_current_fig_manager().window.showMaximized()
plt.show()
plt.close(1)
