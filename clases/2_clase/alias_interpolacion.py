import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
np.set_printoptions(precision=3, suppress=False)

fsC     = 100 #frec de sampleo que imita el 'continuo' cuando mas mejor
fsD     = 10  #frec de sampleo discreta. Como el ejemplo es para una senial de 1hz, segun shanon no se podria recuperar si fsD es menor o igual a 2
N       = 100
signalF = 7

tn   = np.arange(0,N,1)
t    = tn/fsC
td   = tn/fsD

tsinc_n  = np.arange(-N,N,1)
tsinc    = tsinc_n/fsC
nd       = 0

def signal(n):
    return np.sin(2*np.pi*n*signalF) #un seno

x_n     = np.zeros(len(td))
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
lnx_inter, = sigAxe.plot([],[],'g-',linewidth = 10,alpha = 0.5)

def interpolate(timeC, x, B):
    y=[]
    for t in timeC:
        prom=0
        for n in range(len(x)):
           prom += x[n]*np.sinc(2*B*t-n)
        y.append(prom)
    #print("x_n:",x,"t:",2*B*timeC,"y:",y)
    return y

def init():
    global nd
    nd=0
    return lnx_n, lnx_t, lnx_inter, fftLnx_t

def update(n):
    global nd
    #input("wait press")

    if(t[n]>=td[nd]): # instantes de sampleo
        x_n[nd] = signal ( td[nd] )
        lnx_n.set_data(td[:nd+1],x_n[:nd+1])
        plt.plot(td[nd]+tsinc,x_n[nd]*np.sinc(2*(fsD/2)*tsinc),'y-',linewidth=5,alpha=0.2)
        nd+=1

    x_inter=interpolate(t[:n+1],x_n[:nd],fsD/2)
    lnx_inter.set_data(t[0:len(x_inter)],x_inter)

    NN=len(x_inter)
    fd_n = np.arange(-((NN-NN%2)//2),(NN+NN%2)//2,1)
    fd   = fd_n*fsC/NN
    fft=np.abs ( 1/NN*np.fft.fft(x_inter ))**2
    fft=np.fft.fftshift(fft)
    fftAxe.set_ylim ( 0 ,np.max(fft)+0.01)
    fftAxe.set_xlim ( -fsD//2 ,fsD//2 )
    fftLnx_t.set_data ( fd ,fft)
    return lnx_n, lnx_inter, fftLnx_t

ani=FuncAnimation(fig,update,N,init_func=init,blit=False,interval=50,repeat=False)
#mng=plt.get_current_fig_manager()
#mng.resize(mng.window.maxsize())
plt.get_current_fig_manager().window.showMaximized() #para QT5
plt.show()


