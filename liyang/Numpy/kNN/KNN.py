#coding:utf-8
from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group,labels

#KNN算法实现
#用于分类的输人向量是inX,训练样本dataSet,标签向量labels,选择最邻近的数目k
def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0] #4
    diffMat = tile(inX, (dataSetSize,1)) - dataSet  #计算输入向量与每个特征数据的差值,提供的距离计算
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()      #argsort函数返回的是数组值从小到大的索引值
    classCount={}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        # print voteIlabel
        # print classCount.get(voteIlabel,0)
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1 # 对于选举值进行加1的操作
        #对于分类的标签和标签数量排序,降序
        sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
        # print sortedClassCount
    return sortedClassCount[0][0]  #取出第一行第一列,该值为预测的标签

def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    #构造和文件长度一样的为0的数组
    returnMat = zeros((numberOfLines,3)) #构建和数据特征数量一样的为0向量
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()
        listFromLine = line.split('\t')
        # print returnMat
        returnMat[index,:] = listFromLine[0:3]   #逐条更新为0向量
        classLabelVector.append(int(listFromLine[-1]))
        index +=1
    return returnMat,classLabelVector


#数据归一化
#newValue = (oldValue-min)/(max-min)
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    #构建1000,3为0的数组
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet/tile(ranges, (m,1))   #element wise divide
    return normDataSet, ranges, minVals

def classifyPerson():
    resultList = ['not at all','in small doses','in large doses']
    percentTats = float(raw_input("percentage of time spent playing video games?"))
    ffMiles = float(raw_input("frequent flier miles earned per year?"))
    iceCream = float(raw_input("liters of ice cream consumed per year?"))
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
    normMat,ranges,minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles,percentTats,iceCream])
    classifierResult = classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
    print "You will probably like this person:", resultList[classifierResult-1]


def datingClassTest():
    hoRatio = 0.10      #hold out 10%
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')       #load data setfrom file
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio) #100条测试数据
    errorCount = 0.0
    #100条进行算法测试,作为输入向量;  训练数据为900条,包括特征和标签
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]):
            errorCount += 1.0
            print '---------------------------'
    print "the total error rate is: %f" % (errorCount/float(numTestVecs))
    print errorCount




if __name__ == '__main__':
    # group,labels = createDataSet()
    # print group,labels
    # print group.shape[0]
    # a=[[1,2,3],[5,4]]
    # print a
    # print tile([0,0],(4,1))
    # print classify0([0,0],group,labels,3)
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
    # print datingDataMat,datingLabels[0:20]

    #画图
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.scatter(datingDataMat[:,1],datingDataMat[:,2],15.0*array(datingLabels),15.0*array(datingLabels))
    # plt.show()
    # normMat,ranges,minVals = autoNorm(datingDataMat)
    # datingClassTest()
    # print normMat
    # print normMat,ranges,minVals
    classifyPerson()