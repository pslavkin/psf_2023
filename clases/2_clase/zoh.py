import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
np.set_printoptions(precision=3, suppress=False)

fsC     = 100 #frec de sampleo que imita el 'continuo' cuando mas mejor
fsD     = 10  #frec de sampleo discreta. Como el ejemplo es para una senial de 1hz, segun shanon no se podria recuperar si fsD es menor o igual a 2
N       = 100
signalF = 2

fc_n = np.arange(-((N-N%2)//2),(N+N%2)//2,1)
fc   = fc_n*fsC/N

Nd=N*fsD/fsC
fd_n = np.arange(-((Nd-Nd%2)//2),(Nd+Nd%2)//2,1)
fd   = fd_n*fsD/Nd

tn   = np.arange(0,N,1)
t    = tn/fsC
td   = tn/fsD

nd       = 0

def signal(n):
    return np.sin(2*np.pi*n*signalF) #un seno

x_n     = np.zeros(len(t))
x_t     = [signal(i) for i in t]

fig       = plt.figure()
fftAxe    = fig.add_subplot ( 2,1,2      )
fftLnx_t, = plt.plot        ( [],[],'b-',linewidth = 4 )
fftAxe.grid              ( True       )
fftAxe.set_ylim          ( 0 ,0.25 )

sigAxe = fig.add_subplot(2,1,1)
sigAxe.grid(True)
sigAxe.set_xlim(-5/fsC, np.max(t)+1/fsC)
sigAxe.set_ylim(-1,1)

lnx_n,     = sigAxe.plot([],[],'ro',linewidth = 8,alpha  = 0.8)
lnx_t,     = sigAxe.plot(t,x_t,'b-',alpha     = 0.3) #senial original "analogica"


def init():
    global nd
    nd=0
    return lnx_n, lnx_t,  fftLnx_t

def update(n):
    global nd,zoh

    if(t[n]>=td[nd]): # instantes de sampleo
        x_n[n] = signal ( t[n] )
        zoh=x_n[n]
        nd+=1
    else:
        x_n[n] = zoh
#        x_n[n] = -10000

    lnx_n.set_data(t[:n+1],x_n[:n+1])

# esto para sample cada fsD
#    fft=np.abs ( 1/(N/(fsC/fsD))*np.fft.fft(x_n[:N:fsC//fsD]))**2
#    fft=np.fft.fftshift(fft)
#    fftAxe.set_ylim ( 0 ,np.max(fft)+0.01)
#    fftAxe.set_xlim ( -fsD//2 ,fsD//2 )
#    fftLnx_t.set_data ( fd ,fft)

# esto para sample cada fsC
    fft=np.abs ( 1/N*np.fft.fft(x_n ))**2
    fft=np.fft.fftshift(fft)
    fftAxe.set_ylim ( 0 ,np.max(fft)+0.01)
    fftAxe.set_xlim ( -fsC//2 ,fsC//2 )
    fftLnx_t.set_data ( fc ,fft)
    return lnx_n,  fftLnx_t

ani=FuncAnimation(fig,update,N,init_func=init,blit=False,interval=50,repeat=False)
#mng=plt.get_current_fig_manager()
#mng.resize(mng.window.maxsize())
plt.get_current_fig_manager().window.showMaximized() #para QT5
plt.show()


