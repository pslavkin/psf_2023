import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(1)
Nd=20
td = np.linspace(0, 1, Nd)
ax2 = fig.add_subplot(2,2,2)
ax2.plot(td, np.sin(2*np.pi*td),"ro")
ax2.grid(True)

Nc=1000
tc = np.linspace(0, 1, Nc) #probar agregar mas ciclos, la potencia siempre se acota en 0.5
ax1 = fig.add_subplot(2,2,1)
ax1.plot(tc, np.sin(2*np.pi*tc),"b-")
ax1.grid(True)


ax4 = fig.add_subplot(2,2,3)
potc = np.sin(2*np.pi*tc)**2
potcAcum=np.cumsum(potc)
ax4.stem(tc,potcAcum/Nc ,"bo")
ax4.grid(True)

ax4 = fig.add_subplot(2,2,4)
potd = np.sin(2*np.pi*td)**2
potdAcum=np.cumsum(potd)
ax4.stem(td,potdAcum/Nd ,"bo")
ax4.grid(True)

plt.get_current_fig_manager().window.showMaximized() #para QT5
plt.show()
