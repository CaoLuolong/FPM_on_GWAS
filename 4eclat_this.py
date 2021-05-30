# @Time : 2021/5/8 15:51 

# @Author : Larry

# @File : 4eclat_this.py 

# @Software: PyCharm

# -*- coding: utf-8 -*-


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


def rulesFromConseq(freqSet, H, supportData, br1, minConf):
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


# def load_data_set():
#     """
#     Load a sample data set (From Data Mining: Concepts and Techniques, 3th Edition)
#     Returns:
#         A data set: A list of transactions. Each transaction contains several items.
#     """
#     data_set = []
#     with open('result\\49900set0.txt', 'r') as file:  # 所有voxel中显著的SNP集合
#         data = file.read().split(':')
#         for i in range(len(data)-1):
#             data1 = data[i].strip(',').split(',')
#             data_set.append(data1)
#
#     return data_set

# eclat算法
def eclat(prefix, items, min_support, freq_items, set_len):
    while items:
        # 初始遍历单个的元素是否是频繁
        key, item = items.pop()
        key_support = len(item) / float(set_len)
        if key_support >= min_support:
            # print frozenset(sorted(prefix+[key]))
            freq_items[frozenset(sorted(prefix+[key]))] = key_support
            suffix = []  # 存储当前长度的项集
            for other_key, other_item in items:
                new_item = item & other_item  # 求和其他集合求交集
                if len(new_item) >= min_support:
                    suffix.append((other_key, new_item))
            eclat(prefix+[key], sorted(suffix, key=lambda item: len(item[1]), reverse=True), min_support, freq_items, set_len)
    return freq_items


def eclat_zc(data_set, min_support=1):
    """
    Eclat方法
    :param data_set:
    :param min_support:
    :return:
    """
    # 将数据倒排
    data = {}
    trans_num = 0
    set_len = len(data_set)
    for trans in data_set:
        trans_num += 1
        for item in trans:
            if item not in data:
                data[item] = set()
            data[item].add(trans_num)
    freq_items = {}
    freq_items = eclat([], sorted(data.items(), key=lambda item: len(item[1]), reverse=True), min_support, freq_items, set_len)
    return freq_items



# def test_eclat(min_Sup, dataSetDict, dataSet):
#     freqItems = eclat_zc(dataSet, min_Sup)
#     # freqItems = sorted(freqItems.iteritems(), key=lambda item: item[1])
#     return freqItems

def loadDblpData():
    '''
    加载dblp的数据
    :param inFile:
    :return:
    '''
    dataSetDict = {}
    dataSet = []
    count = 0
    with open('result\\37voxel_set_after_pca-rs.txt', 'r') as file:  # 所有voxel中显著的SNP集合
        data = file.read().split(':')
        for i in range(len(data)-1):
            data1 = data[i].strip(',').split(',')
            dataSet.append(data1)
            dataLine = [word for word in data1]
            dataSetDict[frozenset(dataLine)] = dataSetDict.get(frozenset(dataLine), 0) + 1
            count += 1
        return dataSetDict, dataSet

if __name__ == '__main__':

    import numpy
    import sys
    import time
    type = sys.getfilesystemencoding()

    dataSetDict, dataSet = loadDblpData()
    # f = open('result\\49900set0.txt').read().split(":")
    lines = len(dataSet)

    # test_para = numpy.zeros((15, 3))
    # i=0
    # for min_support in numpy.arange(0.4, 0.81, 0.05):
    #     start = time.time()
    #     freqItems = eclat_zc(dataSet, min_support)  # test_eclat(min_Sup, dataSetDict, dataSet)
    #     total_time = time.time() - start
    #     test_para[i,] = [min_support, total_time, len(freqItems)]
    #     i = i+1
    #     print(i, total_time)
    #
    # numpy.savetxt("result/para_time_eclat_roi37.csv",test_para, fmt="%.2f", delimiter=',')

    min_Sup = 0.6
    start = time.time()
    freqItems = eclat_zc(dataSet, min_Sup) # test_eclat(min_Sup, dataSetDict, dataSet)
    print(time.time() - start, 'sec')
    freqItems_sort = sorted(freqItems.items(), key=lambda item: item[1], reverse=True)

    for set, support in freqItems_sort:
        print(set, support)

    freqItems[frozenset([])] = 0.9
    orderedItem = freqItems
    freqItems = [frozenset(x) for x in orderedItem]
    generateRules(freqItems, orderedItem)