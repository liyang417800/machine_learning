#coding:utf-8

from numpy import *

import matplotlib.pyplot as plt

def loadDataSet(fileName):      #打开文件
    numFeat = len(open(fileName).readline().split('\t')) - 1 #得到特征的数量
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr =[]
        curLine = line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat

def standRegres(xArr,yArr):
    xMat = mat(xArr); yMat = mat(yArr).T
    xTx = xMat.T*xMat
    if linalg.det(xTx) == 0.0:
        print "This matrix is singular, cannot do inverse"
        return
    ws = xTx.I * (xMat.T*yMat)
    return ws

def lwlr(testPoint,xArr,yArr,k=1.0):
    xMat = mat(xArr); yMat = mat(yArr).T
    m = shape(xMat)[0]  #获取行数
    weights = mat(eye((m)))  #创建对角权重矩阵
    for j in range(m):                      #next 2 lines create weights matrix
        diffMat = testPoint - xMat[j,:]
        weights[j,j] = exp(diffMat*diffMat.T/(-2.0*k**2))
    xTx = xMat.T * (weights * xMat)
    if linalg.det(xTx) == 0.0:
        print "This matrix is singular, cannot do inverse"
        return
    ws = xTx.I * (xMat.T * (weights * yMat))
    return testPoint * ws

def lwlrTest(testArr,xArr,yArr,k=1.0):  #loops over all the data points and applies lwlr to each one
    m = shape(testArr)[0]
    yHat = zeros(m)
    for i in range(m):
        yHat[i] = lwlr(testArr[i],xArr,yArr,k)
    return yHat

def lwlrTestPlot(xArr,yArr,k=1.0):  #same thing as lwlrTest except it sorts X first
    yHat = zeros(shape(yArr))       #easier for plotting
    xCopy = mat(xArr)
    xCopy.sort(0)
    for i in range(shape(xArr)[0]):
        yHat[i] = lwlr(xCopy[i],xArr,yArr,k)
    return yHat,xCopy

def rssError(yArr,yHatArr): #yArr and yHatArr both need to be arrays
    return ((yArr-yHatArr)**2).sum()

#岭回归调整参数
def ridgeRegres(xMat,yMat,lam=0.2):
    xTx = xMat.T*xMat
    denom = xTx + eye(shape(xMat)[1])*lam
    if linalg.det(denom) == 0.0:
        print "This matrix is singular, cannot do inverse"
        return
    ws = denom.I * (xMat.T*yMat)
    return ws


def ridgeTest(xArr,yArr):
    xMat = mat(xArr); yMat=mat(yArr).T
    yMean = mean(yMat,0) #求的y的平均值9.93368446
    yMat = yMat - yMean     #to eliminate X0 take mean off of Y
    #regularize X's
    xMeans = mean(xMat,0)   #按列求得x的所有特征的平均值
    # print xMeans
    xVar = var(xMat,0)      #按列求方差
    # print xVar
    xMat = (xMat - xMeans)/xVar
    # print xMat
    numTestPts = 30
    wMat = zeros((numTestPts,shape(xMat)[1])) #创建30行8列的为0向量
    for i in range(numTestPts):
        ws = ridgeRegres(xMat,yMat,exp(i-10))
        print ws
        wMat[i,:]=ws.T
    return wMat

def regularize(xMat):#regularize by columns
    inMat = xMat.copy()
    inMeans = mean(inMat,0)   #calc mean then subtract it off
    inVar = var(inMat,0)      #calc variance of Xi then divide by it
    inMat = (inMat - inMeans)/inVar
    return inMat

def stageWise(xArr,yArr,eps=0.01,numIt=100):
    xMat = mat(xArr); yMat=mat(yArr).T
    yMean = mean(yMat,0)
    yMat = yMat - yMean     #can also regularize ys but will get smaller coef
    xMat = regularize(xMat)
    m,n=shape(xMat)
    returnMat = zeros((numIt,n)) #testing code remove
    ws = zeros((n,1))
    wsTest = ws.copy()
    wsMax = ws.copy()
    for i in range(numIt):
        print ws.T
        lowestError = inf;
        for j in range(n):
            for sign in [-1,1]:
                wsTest = ws.copy()
                wsTest[j] += eps*sign
                yTest = xMat*wsTest
                rssE = rssError(yMat.A,yTest.A)
                if rssE < lowestError:
                    lowestError = rssE
                    wsMax = wsTest
        ws = wsMax.copy()
        returnMat[i,:]=ws.T
    return returnMat


if __name__=='__main__':
    xArr,yArr = loadDataSet('ex0.txt')
    # print xArr[0:2] #[[1.0, 0.067732], [1.0, 0.42781]]
    # print mat(xArr[0:2])
    # print yArr[0:2] #[3.176513, 3.816464]
    ws = standRegres(xArr,yArr) #[[ 3.00774324]
                                # [ 1.69532264]]
    xMat = mat(xArr) #转换为矩阵
    yMat = mat(yArr) #转换为矩阵

    yHat = xMat*ws

    fig = plt.figure()
    ax = fig.add_subplot(111)
    # ax.scatter(xMat[:,1].flatten().A[0], yMat.T[:,0].flatten().A[0])
    # xCopy = xMat.copy()
    # xCopy.sort(0)
    # yHat = xCopy*ws  #相乘之后不是矩阵
    # ax.plot(xCopy[:,1],yHat)
    # # plt.show()
    #
    # corrcoef(yHat.T,yMat) #计算相关系数,系数越高匹配度越高

    # print yArr[0]
    # print lwlr(xArr[0],xArr,yArr,1.0)
    # print lwlr(xArr[0],xArr,yArr,0.001)
    yHat =  lwlrTest(xArr,xArr,yArr,0.01)

    srtInd = xMat[:,1].argsort(0) #按照所选列进行升序排列
    # print srtInd
    xSort = xMat[srtInd][:,0,:]
    # print xSort
    # ax.plot(xSort[:,1],yHat[srtInd])
    # ax.scatter(xMat[:,1].flatten().A[0], mat(yArr).T.flatten().A[0],s=2,c='red')
    # plt.show()

    abX,abY = loadDataSet('abalone.txt')
    # yHatO1=lwlrTest(abX[0:99],abX[0:99],abY[0:99],0.1)
    # yHat1=lwlrTest(abX[0:99],abX[0:99],abY[0:99],1)
    # yHat10=lwlrTest(abX[0:99],abX[0:99],abY[0:99],10)

    # yHatO1=lwlrTest(abX[100:199],abX[0:99],abY[0:99],0.1)
    # yHat1=lwlrTest(abX[100:199],abX[0:99],abY[0:99],1)
    # yHat10=lwlrTest(abX[100:199],abX[0:99],abY[0:99],10)
    #
    #
    #
    #
    # print rssError(abY[100:199],yHatO1.T)
    # print rssError(abY[100:199],yHat1.T)
    # print rssError(abY[100:199],yHat10.T)
    #
    # ws = standRegres(abX[0:99],abY[0:99])
    # yHat = mat(abX[100:199])*ws
    # print rssError(abY[100:199],yHat.T.A)
    ridgeWeights = ridgeTest(abX,abY)
    ax.plot(ridgeWeights)
    plt.show()
















