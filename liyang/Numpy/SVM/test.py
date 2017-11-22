import random


def selectJrand(i,m):
    j = i
    while(j==i):
        j = int(random.uniform(0,m))
    return j

def clipAlpha(aj,H,L):
    if aj>H:
        aj = H
    if L>aj:
        aj = L
    return aj

# print selectJrand(1,10)
print clipAlpha(5,6,1)

    # dataArr,labelArr = loadImages('trainingDigits')
    # print dataArr
    # print labelArr
