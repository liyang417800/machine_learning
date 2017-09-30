#coding:utf-8
import operator
from math import log

from sympy import zeros

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

# def createDataSet():
#     dataSet = [[1,1,'yes'],
#                [1,1,'yes'],
#                [1,0,'no'],
#                [0,1,'no'],
#                [0,1,'no']]
#     labels = ['no surfacing','flippers']
#     return dataSet,labels


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

# def createTree(dataSet,labels):
#     classList = [example[-1] for example in dataSet]
#     # print classList
#     if classList.count(classList[0]) == len(classList):
#         return classList[0]
#
#     if len(dataSet[0]) == 1:
#         return majorityCnt(classList)
#
#     bestFeat = chooseBestFeatureToSplit(dataSet)   #选取最好的特征,本实例为[0],第一个特征
#     bestFeatLabel = labels[bestFeat]       #选取最好特征的label
#
#     myTree = {bestFeatLabel:{}}    #构造字典格式{'no surfacing': {}}
#     del(labels[bestFeat])          #删除这次的labels 'no surfacing'
#     featValues = [example[bestFeat] for example in dataSet]  #取出特征[0]的所有值
#
#
#
#     uniqueVals = set(featValues)
#     for value in uniqueVals:
#         subLabels = labels[:]
#         # print splitDataSet(dataSet,bestFeat,value)
#         #[[1, 1, 'yes'], [1, 1, 'yes'], [1, 0, 'no'], [0, 1, 'no'], [0, 1, 'no']]
#         #0
#         #0
#         myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
#         #第一次  {'no surfacing': {0: 'no'}}
#         #第二次 {'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}}
#     return myTree

def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]#stop splitting when all of the classes are equal
    if len(dataSet[0]) == 1: #stop splitting when there are no more features in dataSet
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]       #copy all of labels, so trees don't mess up existing labels
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value),subLabels)
    return myTree

# def classify(inputTree,featLabels,testVec):
#     print inputTree.keys()
#     firstStr = inputTree.keys()[0]
#     secondDict = inputTree[firstStr]
#     #{0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}
#     print 'featLabels.index(firstStr):'+ str(featLabels.index(firstStr))
#     featIndex = featLabels.index(firstStr)
#     print 'testVec[featIndex]:'+ str(testVec[featIndex])
#     key = testVec[featIndex]
#
#     valueOfFeat = secondDict[key]
#     print valueOfFeat
#     if isinstance(valueOfFeat, dict):
#         classLabel = classify(valueOfFeat, featLabels, testVec)
#     else:
#         classLabel = valueOfFeat
#     return classLabel

def classify(inputTree,featLabels,testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    key = testVec[featIndex]
    valueOfFeat = secondDict[key]
    if isinstance(valueOfFeat, dict):
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else: classLabel = valueOfFeat
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

def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    #构造和文件长度一样的为0的数组
    returnMat = []
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat.append (listFromLine[0:9])
        classLabelVector.append(int(listFromLine[-1]))
        index +=1
    return returnMat,classLabelVector


def datingClassTest():
    # hoRatio = 0.10      #hold out 10%
    datingDataMat,datingLabels = file2matrix('is_m4_t.txt')      #load data setfrom file
    # m = normMat.shape[0]
    # numTestVecs = int(m*hoRatio) #100条测试数据
    errorCount = 0.0
    numlen = len(datingDataMat)
    #100条进行算法测试,作为输入向量;  训练数据为900条,包括特征和标签
    fr = open('is_m4.txt')
    lenses = [inst.strip().split() for inst in fr.readlines()]
    lensesLabels = ['gender','marriage','education','house_state','org_type','company_position','city_name','age_desc','income_desc']
    lensesTree = createTree(lenses,lensesLabels)
    # lensesLabels_t = ['gender','marriage','education','house_state','org_type','company_position','city_name','age_desc','income_desc']
    for i in range(numlen):
        lensesLabels_t = ['gender','marriage','education','house_state','org_type','company_position','city_name','age_desc','income_desc']

        classifierResult = classify(lensesTree, lensesLabels_t,datingDataMat[i])
        # print lensesTree
        # print datingDataMat[i]
        # print classifierResult
        print "the classifier came back with: %d, the real answer is: %d" % (int(classifierResult), int(datingLabels[i]))
        if (int(classifierResult) != int(datingLabels[i])):
            errorCount += 1.0
            print '---------------------------'
    print "the total error rate is: %f" % (errorCount/float(numlen))
    print errorCount






if __name__=='__main__':
    # myDat,lables = createDataSet()
    # print splitDataSet(myDat,0,0)
    # print chooseBestFeatureToSplit(myDat)
    # print lables
    # myTree = treePlotter.retrieveTree(0)
    # print myTree
    # myTree = createTree(myDat,lables)

    # print myTree
    # print lables
    # print classify(myTree,lables,[1,1])
    # print myTree
    # storeTree(myTree,'classifierStorage.txt')
    # grabTree('classifierStorage.txt')
    # fr = open('is_m4.txt')
    # lenses = [inst.strip().split() for inst in fr.readlines()]
    # lensesLabels = ['age','prescript','astigmacit','tearRate']
    # lensesLabels = ['gender','marriage','education','house_state','org_type','company_position','city_name','age_desc','income_desc']
    # print lensesLabels
    # lensesTree = createTree(lenses,lensesLabels)
    # print lensesTree
    # lensesLabels = ['gender','marriage','education','house_state','org_type','company_position','city_name','age_desc','income_desc']
    # print lensesLabels
    # treePlotter.createPlot(lensesTree)
    # print(classify(lensesTree, lensesLabels, ['nan','yihun','gaozhongjiyixia','youfangyoudai','minying','gaojiguanlizhe','liaoningsheng','zhongnian','xiaokang']))
    # datingDataMat,datingLabels = file2matrix('is_m4_t.txt')
    # print datingDataMat,datingLabels
    # print len(datingDataMat)
    datingClassTest()





