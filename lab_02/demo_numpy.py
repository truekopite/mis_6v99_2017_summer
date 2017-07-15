
# coding: utf-8

# In[1]:

import numpy as np
import sys

a = np.arange(15).reshape(3,5)
sys.stdout = open("demo_numpy.txt", "w")
print(a)
print(a.shape)
print(a.size)
print(a.itemsize)
print(a.ndim)
print(a.dtype)

