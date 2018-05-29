#coding:utf-8
from numpy import *

def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float,curLine)
        dataMat.append(fltLine)
    return dataMat

def distEclud(vecA,vecB):
    return sqrt(sum(power(vecA - vecB,2)))

def randCent(dataSet,k):
    n = shape(dataSet)[1] #2
    centroids = mat(zeros((k,n))) #k行2列个0
    for j in range(n):
        minJ = min(dataSet[:,j])#获取每一列的最小值
        rangeJ = float(max(dataSet[:,j])-minJ) #每列最大值与最小值的差
        centroids[:,j] = minJ + rangeJ * random.rand(k,1) #差值乘以0到1的随机数
    return centroids

def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    m = shape(dataSet)[0] #数据长度
    clusterAssment = mat(zeros((m,2))) #长度为m的两维为0的mat
    centroids = createCent(dataSet, k)
    print "---"+str(centroids)
    print "---"
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):#for each data point assign it to the closest centroid
            minDist = inf; minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j,:],dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI; minIndex = j
            if clusterAssment[i,0] != minIndex: clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
        print centroids
        for cent in range(k):#recalculate centroids
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]#get all the point in this cluster
            centroids[cent,:] = mean(ptsInClust, axis=0) #assign centroid to mean
    return centroids, clusterAssment


if __name__ =='__main__':
    datMat = mat(loadDataSet('testSet.txt'))
    # print randCent(datMat,2)
    myCentroids,clustAssing = kMeans(datMat,4)









