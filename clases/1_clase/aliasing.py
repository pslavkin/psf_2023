import numpy                as     np
import matplotlib.pyplot    as     plt
from   matplotlib.animation import FuncAnimation
import time
np.set_printoptions(precision=3, suppress=False)

#ejemplo en donde se ve como una senial de exactamente B=fs se esconde en el sampleo
#fsC       = 100 # frec de sampleo que imita el 'continuo' cuando mas mejor
#fsD       = 10   # frec de sampleo discreta. Como el ejemplo es para una senial de 1hz, segun shanon no se podria recuperar si fsD es menor o igual a 2
#sigFrec   = 2
#sigFrecHi = 10 # senial que entra como aliasing
#N         = 200

#ejemplo en donde se ve como una senial de B>fs/2 entra igualmente como ruido en el sampleo
#fsC       = 100 # frec de sampleo que imita el 'continuo' cuando mas mejor
#fsD       = 10   # frec de sampleo discreta. Como el ejemplo es para una senial de 1hz, segun shanon no se podria recuperar si fsD es menor o igual a 2
#sigFrec   = 2
#sigFrecHi = 6 # senial que entra como aliasing
#N         = 200

# ejemplo en donde se ve como los samples con puntos rojos a 11hz, pintan una
# senial de 1hz, 
fsC       = 100 # frec de sampleo que imita el 'continuo' cuando mas mejor
fsD       = 10   # frec de sampleo discreta. Como el ejemplo es para una senial de 1hz, segun shanon no se podria recuperar si fsD es menor o igual a 2
sigFrec   = 6
sigFrecHi = 0 # senial que entra como aliasing
N         = 200

t   = np.arange(0,N/fsC      ,1/fsC)
td  = np.arange(0,N/fsC+1/fsD,1/fsD) #un poquito mas largo para evitar erl redondeo

nd  = 0
s1  = np.zeros(len(td))
s2  = np.zeros(len(t))
s3  = np.zeros(len(t))
s4  = np.zeros(len(t))

fig       = plt.figure()

sigAxe = fig.add_subplot(2,1,1)
sigAxe.grid(True)
sigAxe.set_xlim(0, np.max(t))
sigAxe.set_ylim(-1.2,1.2)
sigLn1, =sigAxe.plot([],[],'ro',markersize=10,linewidth=20,alpha=0.5) # discreta
sigLn2, =sigAxe.plot([],[],'b-',linewidth=1,alpha=1)   # simula la contiua
sigLn3, =sigAxe.plot([],[],'g-',linewidth=3,alpha=0.8) # senial contaminada

fftAxe = fig.add_subplot ( 2,1,2      )
fftAxe.grid              ( True       )
fftAxe.set_ylim          ( 0 ,0.25 )
fftLn, = plt.plot        ( [],[],'b-',linewidth=4 )

def signal(n):
    return np.sin(2*np.pi*n*sigFrec)
def signalHi(n):
    return signal(n)+0.3 * np.sin(2*np.pi*n*sigFrecHi)

def init():
    global nd
    nd=0
    return sigLn1, sigLn2, sigLn3, fftLn

def update(n):
    global nd
    s2[n]=signal(t[n]) #que pasa si agrego ruido
    sigLn2.set_data(t[:n+1],s2[:n+1])

    s3[n]=signalHi(t[n]) #que pasa si agrego ruido
    sigLn3.set_data(t[:n+1],s3[:n+1])

    if(t[n]>=td[nd]):
        s1[nd] = signalHi(td[nd])      #captura
        sigLn1.set_data(td[:nd+1],s1[:nd+1])
        nd+=1

    fft=np.abs ( 1/N*np.fft.fft(s3 ))**2
    fftAxe.set_ylim ( 0 ,np.max(fft)+0.01)
    fftAxe.set_xlim ( 0 ,fsC/2 )
    fftLn.set_data ( (fsC/N )*fsC*t ,fft)
    
    return sigLn1, sigLn2, sigLn3, fftLn


ani=FuncAnimation(fig,update,N,init_func=init,blit=False,interval=10,repeat=False)
#mng=plt.get_current_fig_manager()
#mng.resize(mng.window.maxsize())
plt.get_current_fig_manager().window.showMaximized() #para QT5
plt.show()

