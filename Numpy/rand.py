from numpy import *

randMat = mat(random.rand(4,4))

invRandMat = randMat.I

myEye =  randMat*invRandMat

print myEye - eye(4)

print eye(4)

