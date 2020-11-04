import numpy as np
from math import log
import operator
import matplotlib.pyplot as plt

# 以下定义文本框和箭头格式
decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")
test = "Iris-train.txt"
train = "Iris-test.txt"
# 读取数据函数，np.array类型的测试数据集和训练数据集
# 已知数据集为75*5的大小
testData = np.loadtxt(test)
trainData = np.loadtxt(train)


# 计算信息熵
def calEnt(index, label, step):
    kind = [0, 0, 0]
    EntD = 0
    pk = [0, 0, 0]
    for n in range(step):
        if label[index[n]] == 0:
            kind[0] += 1
        elif label[index[n]] == 1:
            kind[1] += 1
        else:
            kind[2] += 1
    for n in range(3):
        pk[n] = kind[n] / len(label)
        if pk[n] == 0:
            EntD += 0
        else:
            EntD -= pk[n] * log(pk[n], 2)
    return EntD


# dataSet(array类型)返回最大信息增益及其所在的属性和划分值
def bestFeature(dataSet):
    index = []
    for n in range(4):
        index.append(np.argsort(dataSet[:, n], axis=0))
    EntD = calEnt(range(len(dataSet[:, 0])), dataSet[:, -1], len(dataSet[:, 0]))
    T = [[], [], [], []]  # 4个连续属性的候选划分点
    Gain = [[], [], [], []]  # 4个连续属性的候选增益
    for n in range(len(dataSet[:, -1]) - 1):
        for i in range(4):
            T[i].append((dataSet[index[i][n], i] + dataSet[index[i][n + 1], i]) / 2)
            EntDv = [0, 0]
            for j in range(len(dataSet[:, 0]) - 1):
                EntDv[0] = calEnt(index[i][:j + 1], dataSet[:, -1], j + 1)
                EntDv[1] = calEnt(index[i][j + 1:], dataSet[:, -1], len(index[i][j + 1:]))
                Gain[i].append(EntD - ((j + 1) / (len(dataSet[:, 0]) - 1)) * EntDv[0] - (
                        ((len(dataSet[:, 0]) - 1) - (j + 1)) / (len(dataSet[:, 0]) - 1)) * EntDv[1])
    MAX_Gain = [0, 0, 0, 0]
    MAX_index = [0, 0, 0, 0]
    for n in range(4):
        MAX_Gain[n] = max(Gain[n])
        MAX_index[n] = T[n][Gain[n].index(max(Gain[n]))]
    # 最大增益 划分值 所在的属性列
    return max(MAX_Gain), MAX_index[MAX_Gain.index(max(MAX_Gain))], MAX_Gain.index(max(MAX_Gain))


# 根据求得的最大增益，属性，划分值，划分数据集
def splitDataSet(dataSet, value, line):
    smallDataSet = np.empty(shape=(0, 5))
    largeDataSet = np.empty(shape=(0, 5))
    for n in range(len(dataSet[:, -1])):
        if dataSet[n, line] < value:
            smallDataSet = np.append(smallDataSet, [dataSet[n, :]], axis=0)
        else:
            largeDataSet = np.append(largeDataSet, [dataSet[n, :]], axis=0)
    return smallDataSet, largeDataSet


def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount


# 递归
def createTree(dataSet):
    classList = dataSet[:, -1].tolist()
    # 以下返回类别完全相同的
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    # 遍历完所有特征时返回出现次数最多的
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    MaxGain, value, line = bestFeature(dataSet)
    myTree = {line: {}}
    small, large = splitDataSet(dataSet, value, line)
    myTree[line]["-" + str(value)] = createTree(small)
    myTree[line]["+" + str(value)] = createTree(large)
    return myTree


# 获取树的叶子数
def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        # 测试节点的数据类型是否为字典
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs


# 获取树的深度
def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        if thisDepth > maxDepth: maxDepth = thisDepth
    return maxDepth


def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',
                            xytext=centerPt, textcoords='axes fraction',
                            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)


# 在父子节点中填充文本信息
def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)


def plotTree(myTree, parentPt, nodeTxt):
    # 计算宽和高
    numLeafs = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW, plotTree.yOff)
    # 标记子节点属性值
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    # 减小y偏移
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            plotTree(secondDict[key], cntrPt, str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD


def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5 / plotTree.totalW;
    plotTree.yOff = 1.0;
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()


def retrieveTree(i):
    listOfTrees = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                   {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
                   ]
    return listOfTrees[i]


def classify(myTree, testData):
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    testVec = testData
    # 将标签字符串转换为索引
    featIndex = [0, 1, 2, 3].index(firstStr)
    for key in list(secondDict.keys()):
        if float(key) < 0:
            if testVec[featIndex] <= -float(key):
                if type(secondDict[key]).__name__ == 'dict':
                    classLabel = classify(secondDict[key], testVec)
                else:
                    classLabel = secondDict[key]
        else:
            if testVec[featIndex] >= float(key):
                if type(secondDict[key]).__name__ == 'dict':
                    classLabel = classify(secondDict[key], testVec)
                else:
                    classLabel = secondDict[key]
    return classLabel


percent = 0
myTree = createTree(trainData)
for i in range(len(testData[:, -1])):
    if classify(myTree, testData[i, :]) == testData[i, -1]:
        percent += 1
print("正确率:"+str(percent/len(testData[:,-1])))

createPlot(myTree)
