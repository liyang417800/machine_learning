# coding=gbk

from numpy import *

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]         #1代表侮辱性文字,0代表正常言语
    return postingList,classVec

def createVocabList(dataSet):
    vocabSet = set([])  #create empty set
    for document in dataSet:
        vocabSet = vocabSet | set(document) #union of the two sets
    return list(vocabSet)

def setOfWords2Vec(vocabList,inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print 'the word: %s is not in my Vocabulary!' % word
    return returnVec

def bagOfWord2VecMN(vocabList,inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec


def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)  #所有list的数量,list长度为6
    numWords = len(trainMatrix[0])  #一个list的长度,长度为32
    pAbusive = sum(trainCategory) / float(numTrainDocs)  #??
    # p0Num = zeros(numWords)
    # p1Num = zeros(numWords)

    p0Num = ones(numWords)
    p1Num = ones(numWords)

    # p0Denom = 0.0; p1Denom = 0.0
    p0Denom = 2.0; p1Denom = 2.0
    for i in range(numTrainDocs):  #从0开始
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:

            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])

    # p1Vect = p1Num/p1Denom
    # p0Vect = p0Num/p0Denom
    p1Vect = log(p1Num/p1Denom)
    p0Vect = log(p0Num/p0Denom)
    return p0Vect,p1Vect,pAbusive


def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    print '--------',p1
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    print '++++++++',p0

    if p1 > p0:
        return 1
    else:
        return 0

def testingNB():
    listOPosts,listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList,postinDoc))
    p0V,p1V,pAb = trainNB0(trainMat,listClasses)
    print p0V
    print p1V
    print pAb

    testEntry = ['love','my','dalmation']

    thisDoc = array(setOfWords2Vec(myVocabList,testEntry))
    print myVocabList
    print thisDoc
    print testEntry,'classified as :',classifyNB(thisDoc,p0V,p1V,pAb)

    testEntry = ['stupid','garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))

    print testEntry,'classified as :',classifyNB(thisDoc,p0V,p1V,pAb)







if __name__=='__main__':
    listOPosts,listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts) #去重所有的单词
    testingNB()
