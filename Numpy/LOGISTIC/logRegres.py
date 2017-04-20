# coding=gbk
import math
from numpy import *

def loadDataSet():
    dataMat = [];labelMat = []
    fr = open('/Users/yangli/Downloads/machinelearninginaction/Ch05/testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat,labelMat

def sigmoid(inX):
    return 1.0/(1+exp(-inX))

def gradAscent(dataMatIn,classLabels):
    dataMatrix = mat(dataMatIn)
    print dataMatrix
    labelMat = mat(classLabels).transpose()  #行类转至
    print classLabels
    print mat(classLabels)
    print labelMat
    m,n = shape(dataMatrix)
    alpha = 0.001
    maxCycles = 500
    weights = ones((n,1))
    for k in range(maxCycles):
        h = sigmoid(dataMatrix*weights)
        error = (labelMat - h)
        weights = weights + alpha * dataMatrix.transpose() * error
    return weights

if __name__=='__main__':
    dataArr,labelMat = loadDataSet()
    print dataArr
    print labelMat
    gradAscent(dataArr,labelMat)

