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

#合并所有的字符并且去重
def createVocabList(dataSet):
    vocabSet = set([])  #创造空集
    for document in dataSet:
        vocabSet = vocabSet | set(document) #取出两个集合的并集,对于重复的只取一次
    return list(vocabSet)

#判断一个list中所有字符在整个去重集合中是否出现(词向量)
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


#训练函数
def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)  #所有list的数量,list长度为6
    numWords = len(trainMatrix[0])  #一个list的长度,长度为32
    pAbusive = sum(trainCategory) / float(numTrainDocs)  # 3/6
    # p0Num = zeros(numWords)
    # p1Num = zeros(numWords)

    p0Num = ones(numWords)
    p1Num = ones(numWords)

    # p0Denom = 0.0; p1Denom = 0.0
    p0Denom = 2.0; p1Denom = 2.0
    for i in range(numTrainDocs):  #从0开始,计算每个类目的词条的计数总和
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
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)

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


    testEntry = ['love','my','dalmation']

    thisDoc = array(setOfWords2Vec(myVocabList,testEntry))
    print testEntry,'classified as :',classifyNB(thisDoc,p0V,p1V,pAb)

    testEntry = ['aaa','bbb']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))

    print testEntry,'classified as :',classifyNB(thisDoc,p0V,p1V,pAb)

def textParse(bigString):
    import re
    listOfTokens = re.split(r'\W*',bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 0]

def spamTest():
    docList=[];classList=[];fullText=[]
    for i in range(1,26):
        wordList = textParse(open('/Users/yangli/Downloads/machinelearninginaction/Ch04/email/spam/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)


        wordList =textParse(open('/Users/yangli/Downloads/machinelearninginaction/Ch04/email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)

    vocabList = createVocabList(docList)
    trainingSet = range(50); testSet=[]

    #输出测试数据
    for i in range(10):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])

    trainMat = []; trainClasses = []

    for docIndex in trainingSet:

        trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))

        trainClasses.append(classList[docIndex])

    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0

    for docIndex in testSet:
        wordVector = setOfWords2Vec(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
            print "classification error",docList[docIndex]
    print 'the error rate is: ', float(errorCount)/len(testSet)


if __name__=='__main__':
    listOPosts,listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList,postinDoc))
    # print trainMat
    # print len(trainMat)
    # print zeros(32)
    # print sum(listClasses)
    p0V,p1V,pAb = trainNB0(trainMat,listClasses)
    # print p0V,p1V,pAb

    testingNB()
    # spamTest()
    # spamTest()

