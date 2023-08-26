import numpy as np
import scipy.signal as sc
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#--------------------------------------
fig   = plt.figure(1)
fig.suptitle('Deltas lado a lado con su espectro y energia', fontsize=16)
#--------------------------------------
def impulse(n,pos):
    ans=np.zeros(n)
    ans[pos]=1
    return ans

fs    = [1     ,50    ,10    ,10    ]
M     = [10    ,10   ,20    ,5      ]
pos   = [0     ,2     ,5     ,2     ]
scale = [1     ,-3    ,5     ,-10   ]
color = ["bo-" ,"ro-" ,"yo-" ,"co-" ]

for i in range(len(fs)):
    nSequence = np.arange(0,M[i],1)
    tData     = nSequence/fs[i]
    fData     = fs[i]/2-nSequence*fs[i]/M[i]
    xData     = scale[i]*impulse(M[i],pos[i])
    xAxe      = fig.add_subplot(4,2,2*i+1)
    xAxe.grid(True)
    xAxe.set_ylabel("fs={}\nM={}\nshift={}\nscale={}\n".format(fs[i],M[i],pos[i],scale[i]),rotation=0,labelpad=40,fontsize=16,va="center")
    xLn,      = plt.plot(tData,xData,color[i],linewidth = 15,alpha = 0.2)

    fAxe      = fig.add_subplot(4,2,2*i+2)
    fft=np.fft.fftshift(np.fft.fft(xData))
    fftAbs=np.abs((fft/M[i])**2)
    fAxe.set_ylabel("E={0:.2f}".format(sum(fftAbs)),rotation=0,labelpad=30,fontsize=12,va="center")
    fAxe.grid(True)
    fAxe.set_ylim(min([min(fftAbs),min(np.real(fft)),np.min(np.imag(fft))]),
                  max([max(fftAbs),max(np.real(fft)),np.max(np.imag(fft))]))
    fRLn,      = plt.plot(fData,np.real(fft),'b-o',linewidth = 2,alpha = 0.1)
    fILn,      = plt.plot(fData,np.imag(fft),'r-o',linewidth = 2,alpha = 0.1)
    fAbs,      = plt.plot(fData,fftAbs,color[i],linewidth = 6,alpha = 0.7)
plt.get_current_fig_manager().window.showMaximized()
plt.show()
