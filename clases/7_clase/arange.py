import numpy as np
#--------------------------------------
fs          = 17
N           = 12
arange1 = np.arange(0,N,1)/fs
arange2 = np.arange(0,N/fs,1/fs)

print("\narange1:",arange1/fs,"\nlen:",len(arange1))
print("\narange2:",arange2   ,"\nlen:",len(arange2))
