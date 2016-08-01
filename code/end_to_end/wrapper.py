# wrapper.py
import ctypes
import numpy as np
# g++ -c -fPIC function.cpp -o function.o
# g++ -shared -Wl,-soname,library.so -o library.so function.o
# output = ctypes.CDLL('./library.so').function()

# ArrayType = ctypes.c_int*10
# array_pointer = ctypes.cast(output, ctypes.POINTER(ArrayType))
# print np.frombuffer(array_pointer.contents)

# import ctypes
from numpy.ctypeslib import ndpointer

lib = ctypes.CDLL('./library.so')
lib.function.restype = ndpointer(dtype=ctypes.c_int, shape=(10,))

res = lib.function()
print [i for i in res]

# f = ctypes.CDLL('./library.so').function
# f.restype = ctypes.POINTER(ctypes.c_int * 10)
# print [i for i in f().contents]
