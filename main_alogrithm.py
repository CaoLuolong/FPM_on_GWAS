# Date:2020.09
# Author:Gao Yue

# Function:

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 12:44:52 2020

@author: smlz
"""

# coding:utf-8
import apriori_theory
# import time
import numpy as np

# 读取训练集
with open("E:\\plinklwj\\test.csv", "rb") as f:
    dataSet = [line[:-1].split(str.encode(',')) for line in f.readlines()]

# L中的每一个元素都至少在25%的样本中出现过
L, suppData = apriori_theory.apriori.apriori(dataSet, 0.5)  # 阈值越小，越慢

# 生成规则，每个规则的置信度至少是0.6
bigRuleList = apriori_theory.apriori.generateRules(L, suppData, 0.9)

# P→H，根据P集合的大小排序
bigRuleList = sorted(bigRuleList, key=lambda x: len(x[0]), reverse=True)

# 读取测试集
with open("E:\\plinklwj\\test.csv", "rb") as f:
    dataSet = [line[:-1].split(str.encode(',')) for line in f.readlines()]
labels = np.array([int(x[0]) for x in dataSet])

scores = []
for line in dataSet:
    tmp = []
    for item in bigRuleList:
        if item[0].issubset(set(line)):
            if "1" in item[1]:
                tmp.append(float(item[2]))
            # 因为是预测“为1的概率”，所以要用1减
            if "0" in item[1]:
                tmp.append(1 - float(item[2]))
    scores.append(np.mean(tmp))  # 求取均值

scores = list(map(lambda x: x > 0.5, scores))
scores = np.array(scores, dtype='int')
print(sum(np.equal(scores, labels)))
print(len(labels))
print(sum(np.equal(scores, labels)) / float(len(labels)))
