import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sc
import simpleaudio as sa

f    = 6000
fs   = 44100
sec  = 1
B    = 5000
t    = np.arange(0,sec,1/fs)

note = (2**15-1)*np.sin(2 * np.pi * B/2*(t/sec) *t)  #sweept

#steps=10
#note=np.array([])
#for i in range(steps):
#    note=np.append(note,[(2**15-1)*np.sin(2 * np.pi * B*(i/steps) *t)])

#note = (2**15-1)*np.sin(2 * np.pi * B * t)
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

