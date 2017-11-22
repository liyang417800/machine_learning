from numpy import *

def sigmoid(inX):
    return 1.0/(1+exp(-inX))

a=[ 1.00000000e+00 ,-1.76120000e-02,  1.40530640e+01]
b=mat(a)
weights = ones((3,1))
print b
print b*weights

h = sigmoid(b*weights)
print h