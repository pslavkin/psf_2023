import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig        = plt.figure()
fig.suptitle('Transformada inversa como suma de vectores giratorios', fontsize=16)
fs         = 8.0
N          = 8
#--------------------------------------
nData      = np.arange(0,N,1) #arranco con numeros enteros para evitar errores de float
tData      = nData/fs
circleFrec = nData*(fs/N)-fs/2
signalFrec = 1
frecIter   = -1
point      = []
##--------------------------------------
def signal(f,n):
    return 1*np.cos(2*np.pi*f*n*1/fs)# + 0.2j*np.cos(2*np.pi*f*2*n*1/fs)

signalAxe = fig.add_subplot(4,1,1)
signalAxe.set_title("Señal original f={}Hz".format(signalFrec),rotation=0,fontsize=10,va="center")
signalRLn, = plt.plot(tData ,np.real(signal(signalFrec,nData)) ,'b-X' ,linewidth = 3 ,alpha = 1,label="real")
signalILn, = plt.plot(tData ,np.imag(signal(signalFrec,nData)) ,'r-X' ,linewidth = 3 ,alpha = 1,label="imag")
signalAxe.legend()
signalAxe.grid(True)
signalAxe.set_xlim(0,(N-1)/fs)
signalAxe.set_ylim(np.min(np.real(signal(signalFrec,nData)))-0.1,np.max(np.real(signal(signalFrec,nData)))+0.1)
#--------------------------------------
fftAxe   = fig.add_subplot(4,1,2)
fftAxe.set_title("Espectro DFT(signal)",rotation=0,fontsize=10,va="center")
fftData  = np.fft.fftshift(np.fft.fft(signal(signalFrec,nData)))/N
fftDataR = np.fft.fftshift(np.real(np.fft.fft(signal(signalFrec,nData))))/N
fftDataI = np.fft.fftshift(np.imag(np.fft.fft(signal(signalFrec,nData))))/N
fftRLn,  = plt.plot(circleFrec , (fftDataR) ,'b-X' ,linewidth = 6 ,alpha = 0.3,label="real")
fftILn,  = plt.plot(circleFrec , (fftDataI) ,'r-X' ,linewidth = 6 ,alpha = 0.3,label="imag")
fftAxe.legend()
#-------------------------------------
circleAxe    = []
circleLn     = []
for i in range(N):
    circleAxe.append(fig.add_subplot(4,N,(i+1)+2*N))
    circleLn.append(plt.plot([0,0] ,[0,0] ,'ro-' ,linewidth = 3,alpha=0.5,label="{}".format(i))[0])
    circleAxe[i].axes.get_xaxis().set_visible(False)
    circleAxe[i].axes.get_yaxis().set_visible(False)
    circleAxe[i].set_xlim(-1,1)
    circleAxe[i].set_ylim(-1,1)
    circleAxe[i].legend()

def circle(f,n):
    return np.exp(1j*2*np.pi*f*n*1/fs)
#--------------------------------------
ifftAxe=fig.add_subplot(4,1,4)
ifftAxe.set_title("Anti transformada como suma de vectores",rotation=0,fontsize=10,va="center")
ifftAxe.set_xlim ( 0,(N-1)/fs )
ifftAxe.set_ylim ( -1,1     )
sumaRLn,  = plt.plot([], [] ,'b-X' ,linewidth = 12 ,alpha = 0.5)
sumaILn,  = plt.plot([], [] ,'r-X' ,linewidth = 12 ,alpha = 0.5)
sumaData = np.zeros(N).astype("complex")
ifftAxe.set_xlim(0,(N-1)/fs)
ifftAxe.set_ylim(np.min(np.real(signal(signalFrec,nData)))-0.1,np.max(np.real(signal(signalFrec,nData)))+0.1)
ifftPointRLn, = plt.plot([], [] ,'k-o' ,linewidth = 12 ,alpha = 1)
ifftPointILn, = plt.plot([], [] ,'k-o' ,linewidth = 12 ,alpha = 1)

def init():
    return sumaRLn,

def update(n):
    input()
    point=[]
    for i in range(N):
        point.append(circle(circleFrec[i],n)*fftData[i])
        circleLn[i].set_data([0,np.real(point[i])] ,
                             [0,np.imag(point[i])])
    sumaData[n]=np.sum(point)
    sumaRLn.set_data(tData,np.real(sumaData))
    sumaILn.set_data(tData,np.imag(sumaData))

    ifftPointRLn.set_data(tData[n],np.real(sumaData[n]))
    ifftPointILn.set_data(tData[n],np.imag(sumaData[n]))

    return circleLn,sumaRLn,sumaILn,ifftPointRLn,ifftPointILn,


ani=FuncAnimation(fig,update,N,init,interval=1000 ,blit=False,repeat=False)
plt.get_current_fig_manager().window.showMaximized()
plt.show()
