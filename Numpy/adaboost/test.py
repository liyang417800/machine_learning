from numpy import *

def loadSimpData():
    datMat = matrix([[1.,2.1],
                     [2.,1.1],
                     [1.3,1.],
                     [1.,1.],
                     [2.,1.]])
    classLabels = [1.0,1.0,-1.0,-1.0,-1.0]

    return datMat,classLabels


def stumpClassify(dataMatrix,dimen,threshVal,threshIneq):
    # dimen 0; threshval 0.9; threshIneq ['lt', 'gt']
    retArray = ones((shape(dataMatrix)[0],1))

    if threshIneq == 'It':
        retArray[dataMatrix[:,dimen]<=threshVal] = -1.0
        print retArray
    else:
        retArray[dataMatrix[:,dimen]>threshVal] = -1.0
        print retArray
    return retArray

if __name__=='__main__':
    datMat,classLabels = loadSimpData()
    print stumpClassify(datMat,0,0.9,'It')