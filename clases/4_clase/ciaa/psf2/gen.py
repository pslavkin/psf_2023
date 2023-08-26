import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sc
import simpleaudio as sa

fs   = 44100
sec  = 1
t    = np.arange(0,sec,1/fs)

note=np.zeros(len(t))
L=110  #tiene que matchear con la señal creada en la CIAA
OFFSET=1000
for i in range(L):
    note[i+OFFSET]=-(2**15-1)*i/L
for i in range(L,L+L):
    note[i+OFFSET]=(2**15-1)*(i-L)/L

#probar agregarndo ruido
note+=np.random.normal(0,((2**15)-1)/5,len(t))

fig=plt.figure(1)
plt.plot(t,note)
plt.show()

audio = note.astype(np.int16)
for i in range(1000):
    play_obj = sa.play_buffer(audio, 1, 2, fs)
    play_obj.wait_done()

