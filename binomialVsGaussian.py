from scipy.stats import *
import numpy as np
import matplotlib.pyplot as plt

p = 0.7083
q = 1 - p
n = 20000
std = np.sqrt(n*p*q)
ptest = 0.6899
ztest = n*(p-ptest)/std

gauss = 1-norm.cdf(ztest)
bin = binom.cdf(ptest*n,n,p)
print(gauss/bin)
