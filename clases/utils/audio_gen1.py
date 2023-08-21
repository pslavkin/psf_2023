import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sc
import simpleaudio as sa

f    = 500
fs   = 44100
sec  = 5
B    = 1000
startF = 0
t    = np.arange(0,sec,1/fs)
z    = np.zeros(len(t))

note = (2**15-1)*np.sin(2 * np.pi * (B/2*(t/sec) +startF) *t)  #sweept

#steps=10
#note=np.array([])
#for i in range(steps):
#    note=np.append(note,[(2**15-1)*np.sin(2 * np.pi * B*(i/steps) *t)])

#note = (2**15-1)*np.sin(2 * np.pi * f * t)
#note = (2**15-1)*sc.sawtooth(2 * np.pi * f * t)
#note = (2**15-1)*sc.square(2 * np.pi * f * t)


#fig=plt.figure(1)
#plt.plot(t,note)
##plt.plot(t[0:5*fs//f],note[:5*fs//f])
#plt.show()

audio = note.astype(np.int16)
for i in range(1000):
    play_obj = sa.play_buffer(audio, 1, 2, fs)
    play_obj.wait_done()

