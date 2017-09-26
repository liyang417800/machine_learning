import matplotlib.pyplot as plt

decisionNode = dict(boxstyle='sawtooth',fc='0.8')

leafNode = dict(boxstyle='round4',fc='0.8')

arrow_args = dict(arrowstyle='<-')

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt,  xycoords='axes fraction',
             xytext=centerPt, textcoords='axes fraction',
             va="center", ha="center", bbox=nodeType, arrowprops=arrow_args )


def createPlot():
    fig = plt.figure(1,facecolor='white')
    fig.clf()
    createPlot.ax1 = plt.subplot(111,frameon=False)
    plotNode('a decision node',(0.5,0.1),(0.1,0.5),decisionNode)
    plotNode('a leaf node',(0.8,0.1),(0.3,0.8),leafNode)
    plt.show()

#{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}
def getNumLeafs(myTree):
    numLeafs = 0
    print myTree.keys()
    firstStr = myTree.keys()[0]
    print 'firstStr:'+str(firstStr)
    secondDict = myTree[firstStr]
    print 'secondDict:'+str(secondDict)
    print 'secondDict.keys:'+str(secondDict.keys())
    for key in secondDict.keys():
        print secondDict[key]
        print type(secondDict[key]).__name__
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
            print numLeafs
    return numLeafs

def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1+getTreeDepth(secondDict[key])
        else:
            thisDepth =1
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    return maxDepth

def retrieveTree(i):
    listOfTrees =[{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                  {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
                  ]
    return listOfTrees[i]










if __name__=='__main__':
    createPlot()
    myTree=retrieveTree(0)
    print myTree
    print getNumLeafs(myTree)
    print getTreeDepth(myTree)