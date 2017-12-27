# -*- coding: utf-8 -*-

from numpy import *



def loadSimpData():
    datMat = matrix([[ 1. ,  2.1],
        [ 2. ,  1.1],
        [ 1.3,  1. ],
        [ 1. ,  1. ],
        [ 2. ,  1. ]])
    classLabels = [1.0, 1.0, -1.0, -1.0, 1.0]
    return datMat,classLabels

def stumpClassify(dataMatrix,dimen,threshVal,threshIneq):#just classify the data
    retArray = ones((shape(dataMatrix)[0],1))
    if threshIneq == 'lt':
        retArray[dataMatrix[:,dimen] <= threshVal] = -1.0
    else:
        retArray[dataMatrix[:,dimen] > threshVal] = -1.0
    return retArray

#找到最低错误率的单层决策树
def buildStump(dataArr,classLabels,D):
    dataMatrix = mat(dataArr); labelMat = mat(classLabels).T
    m,n = shape(dataMatrix)
    numSteps = 10.0
    bestStump = {}
    bestClasEst = mat(zeros((m,1)))
    minError = inf #正无穷
    for i in range(n):#loop over all dimensions
        rangeMin = dataMatrix[:,i].min() #1
        rangeMax = dataMatrix[:,i].max() #2
        stepSize = (rangeMax-rangeMin)/numSteps  #0.1
        for j in range(-1,int(numSteps)+1):#loop over all range in current dimension
            for inequal in ['lt', 'gt']: #go over less than and greater than
                threshVal = (rangeMin + float(j) * stepSize)  #fisrt 0.9
                predictedVals = stumpClassify(dataMatrix,i,threshVal,inequal)#call stump classify with i, j, lessThan
                errArr = mat(ones((m,1)))
                errArr[predictedVals == labelMat] = 0
                weightedError = D.T*errArr  #calc total error multiplied by D

                #print "split: dim %d, thresh %.2f, thresh ineqal: %s, the weighted error is %.3f" % (i, threshVal, inequal, weightedError)
                if weightedError < minError:
                    minError = weightedError
                    bestClasEst = predictedVals.copy()
                    # print bestClasEst
                    bestStump['dim'] = i
                    bestStump['thresh'] = threshVal
                    bestStump['ineq'] = inequal
                    # print bestStump
    return bestStump,minError,bestClasEst  #单层最佳决策树,最小错误率,预测的结果

#返回单层决策树的训练过程
def adaBoostTrainDS(dataArr,classLabels,numIt=40):
    weakClassArr = []
    m = shape(dataArr)[0]
    D = mat(ones((m,1))/m)   #init D to all equal
    # print D
    aggClassEst = mat(zeros((m,1)))
    for i in range(numIt):
        bestStump,error,classEst = buildStump(dataArr,classLabels,D)#build Stump
        # print "D:",D.T
        alpha = float(0.5*log((1.0-error)/max(error,1e-16)))#calc alpha, throw in max(error,eps) to account for error=0
        bestStump['alpha'] = alpha
        weakClassArr.append(bestStump)                  #store Stump Params in Array
        # print weakClassArr
        # print "classEst: ",classEst.T
        expon = multiply(-1*alpha*mat(classLabels).T,classEst) #
        # print expon
        D = multiply(D,exp(expon))                              #Calc New D for next iteration
        # print D
        D = D/D.sum()
        # print D
        #calc training error of all classifiers, if this is 0 quit for loop early (use break)
        aggClassEst += alpha*classEst
        # print "aggClassEst: ",aggClassEst.T
        aggErrors = multiply(sign(aggClassEst) != mat(classLabels).T,ones((m,1)))
        errorRate = aggErrors.sum()/m
        print "total error: ",errorRate
        if errorRate == 0.0: break
    return weakClassArr

#输入待分类的算法,加载训练好的弱分类器,对于数据进行分类
def adaClassify(datToClass,classifierArr):
    dataMatrix = mat(datToClass)#do stuff similar to last aggClassEst in adaBoostTrainDS
    m = shape(dataMatrix)[0]
    aggClassEst = mat(zeros((m,1)))
    for i in range(len(classifierArr)):
        classEst = stumpClassify(dataMatrix,classifierArr[i]['dim'],\
                                 classifierArr[i]['thresh'],\
                                 classifierArr[i]['ineq'])#call stump classify

        aggClassEst += classifierArr[i]['alpha']*classEst  #每次加载一个弱分类器对于待分类数据分类,然后循环叠加
        print 'aggClassEst:'+aggClassEst.__str__()
    return sign(aggClassEst)


def loadDataSet(fileName):
    numFeat = len(open(fileName).readline().split('\t'))
    dataMat = []; labelMat = []
    fr = open(fileName)

    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split('\t')
        for i in range(numFeat-1):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat


if __name__=='__main__':
    # datMat,classLabels = loadSimpData()
    # print datMat,classLabels
    D= mat(ones((5,1))/5)
    # print D
    # print buildStump(datMat,classLabels,D)
    # print adaBoostTrainDS(datMat,classLabels,9)
    datArr,labelArr = loadDataSet('horseColicTraining2.txt')
    # print datArr,labelArr
    classifierArray =  adaBoostTrainDS(datArr,labelArr,50)

    #
    testArr,testLabelArr = loadDataSet('horseColicTest2.txt')
    # print 'classifierArray:'+classifierArray.__str__()
    prediction10 = adaClassify(testArr,classifierArray)
    print 'prediction10:'+prediction10.__str__()
    errArr = mat(ones((67,1)))

    print (errArr[prediction10 != mat(testLabelArr).T].sum()/len(testArr)*100).__str__()+'%'










