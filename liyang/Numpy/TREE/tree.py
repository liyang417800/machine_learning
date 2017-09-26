#coding:utf-8
import operator
from math import log

import treePlotter

#计算熵
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLbel = featVec[-1]
        if currentLbel not in labelCounts.keys():  #从0开始计数新的类
            labelCounts[currentLbel] = 0
        labelCounts[currentLbel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -=prob * log(prob,2)  #log以2为底1的对数为0
    return shannonEnt

def createDataSet():
    dataSet = [[1,1,'yes'],
               [1,1,'yes'],
               [1,0,'no'],
               [0,1,'no'],
               [0,1,'no']]
    labels = ['no surfacing','flippers']
    return dataSet,labels


#按照list位置和value获取对应的值
def splitDataSet(dataSet,axis,value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet
#选出最好的feature
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1      #the last column is used for the labels
    baseEntropy = calcShannonEnt(dataSet)  #原始熵0.970950594455
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):        #features数量为2
        featList = [example[i] for example in dataSet]#create a list of all the examples of this feature
        #[1, 1, 1, 0, 0]
        uniqueVals = set(featList)       #get a set of unique values
        newEntropy = 0.0
        #计算信息熵
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value) #第一次 (dataSet,0,1)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy     #计算信息增益
        if (infoGain > bestInfoGain):       #compare this to the best gain so far
            bestInfoGain = infoGain         #if better than current best, set to best
            bestFeature = i
    return bestFeature


def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    print classList
    print classList.count(classList[0])
    print len(classList)
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    print dataSet[0]
    print len(dataSet[0])
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)

    bestFeat = chooseBestFeatureToSplit(dataSet)   #选取最好的特征,本实例为[0],第一个特征
    print bestFeat
    bestFeatLabel = labels[bestFeat]       #选取最好特征的label
    print bestFeatLabel

    myTree = {bestFeatLabel:{}}    #构造字典格式{'no surfacing': {}}
    print 'myTree:'+str(myTree)
    del(labels[bestFeat])          #删除这次的labels 'no surfacing'
    featValues = [example[bestFeat] for example in dataSet]  #取出特征[0]的所有值
    print featValues


    uniqueVals = set(featValues)
    print uniqueVals
    for value in uniqueVals:
        subLabels = labels[:]
        print 'subLabels:'+str(subLabels)
        print 'bestFeatLabel:' +str(bestFeatLabel)
        print dataSet
        print bestFeat
        print value
        # print splitDataSet(dataSet,bestFeat,value)
        #[[1, 1, 'yes'], [1, 1, 'yes'], [1, 0, 'no'], [0, 1, 'no'], [0, 1, 'no']]
        #0
        #0
        print splitDataSet(dataSet,bestFeat,value)
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
        #第一次  {'no surfacing': {0: 'no'}}
        #第二次 {'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}}
        print
    return myTree

def classify(inputTree,featLabels,testVec):
    print inputTree.keys()
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    #{0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}
    print 'featLabels.index(firstStr):'+ str(featLabels.index(firstStr))
    featIndex = featLabels.index(firstStr)
    print 'testVec[featIndex]:'+ str(testVec[featIndex])
    key = testVec[featIndex]

    valueOfFeat = secondDict[key]
    print valueOfFeat
    if isinstance(valueOfFeat, dict):
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else:
        classLabel = valueOfFeat
    return classLabel

# ['no surfacing', 'flippers']
# {'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}}

def storeTree(inputTree,filename):
    import pickle
    fw = open(filename,'w')
    pickle.dump(inputTree,fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)










if __name__=='__main__':
    myDat,lables = createDataSet()
    print myDat,lables
    # #熵等于0.970950594455
    print calcShannonEnt(myDat)
    print splitDataSet(myDat,0,0)
    print chooseBestFeatureToSplit(myDat)
    # # myTree = createTree(myDat,lables)
    # # print myTree
    # myTree1 = treePlotter.retrieveTree(0)
    # print myTree1
    # print lables
    # print classify(myTree1,lables,[1,1])
    #
    # print myTree
    # storeTree(myTree,'classifierStorage.txt')
    # grabTree('classifierStorage.txt')
    # fr = open('lenses.txt')
    # lenses = [inst.strip().split() for inst in fr.readlines()]
    # print(lenses)
    # lensesLabels = ['age','prescript','astigmacit','tearRate']
    # lensesTree = createTree(lenses,lensesLabels)
    # print lensesTree



