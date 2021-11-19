# @Time : 2021/5/7 22:10 

# @Author : Larry

# @File : 3fpgrowth_this.py 

# @Software: PyCharm


# coding:utf-8
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):
        # print('-' * ind, self.name, '-', self.count)
        for child in self.children.values():
            child.disp(ind + 1)


def updateHeader(nodeToTest, targetNode):
    while nodeToTest.nodeLink != None:
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def updateFPtree(items, inTree, headerTable, count):
    if items[0] in inTree.children:
        # 判断items的第一个结点是否已作为子结点
        inTree.children[items[0]].inc(count)
    else:
        # 创建新的分支
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        # 更新相应频繁项集的链表，往后添加
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    # 递归
    if len(items) > 1:
        updateFPtree(items[1::], inTree.children[items[0]], headerTable, count)


def createFPtree(dataSet, minSup=1):
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    for k in list(headerTable.keys()):
        if headerTable[k] < minSup:
            del (headerTable[k])  # 删除不满足最小支持度的元素
    freqItemSet = set(headerTable.keys())  # 满足最小支持度的频繁项集
    if len(freqItemSet) == 0:
        return None, None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]  # element: [count, node]

    retTree = treeNode('Null Set', 1, None)
    for tranSet, count in dataSet.items():
        # dataSet：[element, count]
        localD = {}
        for item in tranSet:
            if item in freqItemSet:  # 过滤，只取该样本中满足最小支持度的频繁项
                localD[item] = headerTable[item][0]  # element : count
        if len(localD) > 0:
            # 根据全局频数从大到小对单样本排序
            # orderedItem = [v[0] for v in sorted(localD.iteritems(), key=lambda p:(p[1], -ord(p[0])), reverse=True)]
            orderedItem = [v[0] for v in sorted(localD.items(), key=lambda p: (p[1], int(p[0])), reverse=True)]
            # 用过滤且排序后的样本更新树
            updateFPtree(orderedItem, retTree, headerTable, count)
    return retTree, headerTable


# 回溯
def ascendFPtree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendFPtree(leafNode.parent, prefixPath)


# 条件模式基
def findPrefixPath(basePat, myHeaderTab):
    treeNode = myHeaderTab[basePat][1]  # basePat在FP树中的第一个结点
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendFPtree(treeNode, prefixPath)  # prefixPath是倒过来的，从treeNode开始到根
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count  # 关联treeNode的计数
        treeNode = treeNode.nodeLink  # 下一个basePat结点
    return condPats


def mineFPtree(inTree, headerTable, minSup, preFix, freqItemList):
    # 最开始的频繁项集是headerTable中的各元素
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]  # 根据频繁项的总频次排序
    for basePat in bigL:  # 对每个频繁项
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable)  # 当前频繁项集的条件模式基
        myCondTree, myHead = createFPtree(condPattBases, minSup)  # 构造当前频繁项的条件FP树
        if myHead != None:
            mineFPtree(myCondTree, myHead, minSup, newFreqSet, freqItemList)  # 递归挖掘条件FP树


# def loadSimpDat():
#     simDat = [['r','z','h','j','p'],
#               ['z','y','x','w','v','u','t','s'],
#               ['z'],
#               ['r','x','n','o','s'],
#               ['y','r','x','z','q','t','p'],
#               ['y','z','x','e','q','s','t','m']]
#     return simDat
def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        key = frozenset(trans)
        if key in retDict:
            retDict[frozenset(trans)] += 1
        else:
            retDict[frozenset(trans)] = 1
    return retDict


def calSuppData(headerTable, freqItemList, total):
    suppData = {}
    for Item in freqItemList:
        # 找到最底下的结点
        Item = sorted(Item, key=lambda x: headerTable[x][0])
        base = findPrefixPath(Item[0], headerTable)
        # 计算支持度
        support = 0
        for B in base:
            if frozenset(Item[1:]).issubset(set(B)):
                support += base[B]
        # 对于根的儿子，没有条件模式基
        if len(base) == 0 and len(Item) == 1:
            support = headerTable[Item[0]][0]

        suppData[frozenset(Item)] = support / float(total)
    return suppData


def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[:k - 2];
            L2 = list(Lk[j])[:k - 2]
            L1.sort();
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList


def calcConf(freqSet, H, supportData, br1, minConf=0.7):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            print("{0} --> {1} conf:{2}".format(freqSet - conseq, conseq, conf))
            br1.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH


def rulesFromConseq(freqSet, H, supportData, br1, minConf=0.7):
    m = len(H[0])
    if len(freqSet) > m + 1:
        Hmp1 = aprioriGen(H, m + 1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, br1, minConf)
        if len(Hmp1) > 1:
            rulesFromConseq(freqSet, Hmp1, supportData, br1, minConf)


def generateRules(freqItemList, supportData, minConf=0.7):
    bigRuleList = []
    for freqSet in freqItemList:
        H1 = [frozenset([item]) for item in freqSet]
        if len(freqSet) > 1:
            rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
        else:
            calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList


def load_data_set():
    """
    Load a sample data set (From Data Mining: Concepts and Techniques, 3th Edition)
    Returns:
        A data set: A list of transactions. Each transaction contains several items.
    """

    data_set = []
    with open('result\\37voxel_set_after_pca.txt', 'r') as file:  # 所有voxel中显著的SNP集合
        data = file.read().split(':')
        for i in range(len(data) - 1):
            data1 = data[i].strip(',').split(',')
            data_set.append(data1)

    return data_set


if __name__ == "__main__":
    import time
    import numpy

    # '''simple data'''
    # simDat = fpgrowth.loadSimpDat()
    # initSet = fpgrowth.createInitSet(simDat)
    # myFPtree, myHeaderTab = fpgrowth.createFPtree(initSet, 3)
    # myFPtree.disp()

    '''kosarak data'''
    start = time.time()
    initSet = []

    parsedDat = load_data_set()

    test_para = numpy.zeros((15, 3))
    i = 0

    start = time.time()
    n = 0.4 * len(parsedDat)  # 用数据集构造FP树，最小支持度10w
    initSet = createInitSet(parsedDat)
    myFPtree, myHeaderTab = createFPtree(initSet, n)
    myFPtree.disp()
    # 挖掘FP树
    freqItems = []
    mineFPtree(myFPtree, myHeaderTab, n, set([]), freqItems)
    suppData = calSuppData(myHeaderTab, freqItems, len(parsedDat))
    suppData[frozenset([])] = 0.9

    for min_support in numpy.arange(0.4, 0.81, 0.05):
        orderedItem = {k: v for k, v in suppData.items() if
                       (v >= min_support and len(k) == 1)}  # find all the 1-item FITs
        # orderedItem = {k: v for k, v in suppData.items() if v >= min_support}  # find all the FITs
        total_time = time.time() - start
        test_para[i,] = [min_support, total_time, len(orderedItem)]
        i = i + 1
        print(i, total_time)

    numpy.savetxt("result/para_time_fpgrowth37k=1.csv", test_para, fmt="%.2f", delimiter=',')

    # start = time.time()
    # n = 0.4 * len(parsedDat)  # 用数据集构造FP树，最小支持度10w
    # initSet = createInitSet(parsedDat)
    # myFPtree, myHeaderTab = createFPtree(initSet, n)
    # myFPtree.disp()
    # # 挖掘FP树
    # freqItems = []
    # mineFPtree(myFPtree, myHeaderTab, n, set([]), freqItems)
    #
    # # compute support values of freqItems
    # suppData = calSuppData(myHeaderTab, freqItems, len(parsedDat))
    # suppData[frozenset([])] = 0.9
    # print(time.time()-start, 'sec')
    # orderedItem = {k:v for k,v in suppData.items() if v >= 0.5}
    # orderedItem_sort = sorted(orderedItem.items(), key=lambda item: item[1], reverse=True)
    #
    #
    # snp_name = []
    # with open('result\\ADNI_voxel_AD_IGAP33_VBM.bim', 'r') as file:
    #     data = file.read().split('\n')
    #     for i in range(len(data)-1):
    #         data1 = data[i].split('\t')[1]
    #         snp_name.append(data1)
    #
    # for x,v in orderedItem_sort:
    #     print(x, v)
    # print("association rules =" * 50)
    # # print({x: v for x, v in orderedItem.items()})
    # freqItems = [frozenset(x) for x in orderedItem]
    # generateRules(freqItems, orderedItem)
