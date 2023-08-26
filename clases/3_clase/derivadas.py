import numpy as np
import matplotlib.pyplot as plt

N    = 100
dx   = 0.1
t    = np.arange(0,dx*N,dx)
f    = [t,
        2**t,
        3**t,
        np.exp(t),
        ]

fig  = plt.figure()

for i in range(len(f)):
    contiAxe = fig.add_subplot(2,2,i+1)
    y=np.real(np.diff(f[i])/dx)
    plt.plot(t,np.real(f[i]),'r-',linewidth=10,alpha=0.3)
    plt.plot(t[:-1],y,'b-')

plt.show()
