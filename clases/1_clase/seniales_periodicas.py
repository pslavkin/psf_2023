from sys import getsizeof
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=3, suppress=False)

#a list
listA=[1,2,3]
print(listA,type(listA))

#append con listas
listA.append(4)

listB=[3,2,1]
listC=listA+listB #concatena listas
print(listC)

#pythonic way to fill a list
listD=[np.sin(2*np.pi*3*t*1/30) for t in range(20)]
print(listD)

#numpy arrays
arrA = np.array([20,10,30]) #array de 3
print(arrA,type(arrA),type(arrA[0]))

arrA8 = np.array([20,10,30]).astype(np.uint8) #array de 3

#repetir con numpy
arrB  = np.tile(arrA,3)        #replica un array n veces
print(arrB)

#append/concatenate con numpy
arrC=np.append(arrB,arrB)
print(arrC,len(arrC))

#bases de tiempo
#--------------------
#arange asegura el paso
t=np.arange(0,len(listD),1) #base de tiempo de 0 a 3 (no inclusive) en pasos de 1
print(len(t),t,getsizeof(t))

#linspace asegura la cantidad de valores
t = np.linspace (0 ,len(listD) ,len(listD))
print(len(t) ,t ,getsizeof(t))

#grafico con matplotlib
plt.plot(t,listD,'ro-')
plt.show()

#generators
t=(i**2 for i in range(9))
print(next(t),next(t),next(t))

#generators con funciones
def signal(frec,fs):
    t=0
    while True:
        yield np.sin(2*np.pi*frec*t*1/fs)
        t+=1

a=signal(3,20)
s=np.array([next(a) for i in range(9)])

#generators in line
a=(np.sin(2*np.pi*3*t*1/20) for t in range(100))
s=np.array([next(a) for i in range(100)])

