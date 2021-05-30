# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 09:00:12 2020

"""
import numpy





def create_C1(data_set):
    """
    Create frequent candidate 1-itemset C1 by scaning data set.
    Args:
        data_set: A list of transactions. Each transaction contains several items.
    Returns:
        C1: A set which contains all frequent candidate 1-itemsets
    """
    C1 = set()
    for t in data_set:
        for item in t:
            item_set = frozenset([item])
            C1.add(item_set)
    return C1


def is_apriori(Ck_item, Lksub1):
    """
    Judge whether a frequent candidate k-itemset satisfy Apriori property.
    Args:
        Ck_item: a frequent candidate k-itemset in Ck which contains all frequent
                 candidate k-itemsets.
        Lksub1: Lk-1, a set which contains all frequent candidate (k-1)-itemsets.
    Returns:
        True: satisfying Apriori property.
        False: Not satisfying Apriori property.
判断频繁候选k项集是否满足先验性质。
参数：
Ck_item：Ck中一个包含所有频繁候选k项集的频繁候选k项集。
Lksub1:Lk-1，包含所有频繁候选（k-1）项集的集合。
返回：
True：满足先验属性。
False：不满足Apriori属性。
    """
    for item in Ck_item:
        sub_Ck = Ck_item - frozenset([item])
        if sub_Ck not in Lksub1:
            return False
    return True


def create_Ck(Lksub1, k):
    """
    Create Ck, a set which contains all all frequent candidate k-itemsets
    by Lk-1's own connection operation.
    Args:
        Lksub1: Lk-1, a set which contains all frequent candidate (k-1)-itemsets.
        k: the item number of a frequent itemset.
    Return:
        Ck: a set which contains all all frequent candidate k-itemsets.
Create Ck，通过Lk-1自身的连接操作，包含所有频繁候选k项集的集合。
参数：
Lksub1:Lk-1，包含所有频繁候选（k-1）项集的集合。
k： 频繁项集的项号。
返回：
Ck：包含所有频繁候选k项集的集合。
    """
    Ck = set()
    len_Lksub1 = len(Lksub1)
    list_Lksub1 = list(Lksub1)
    for i in range(len_Lksub1):
        for j in range(1, len_Lksub1):
            l1 = list(list_Lksub1[i])
            l2 = list(list_Lksub1[j])
            l1.sort()
            l2.sort()
            if l1[0:k - 2] == l2[0:k - 2]:
                Ck_item = list_Lksub1[i] | list_Lksub1[j]
                # pruning
                if is_apriori(Ck_item, Lksub1):
                    Ck.add(Ck_item)
    return Ck


def generate_Lk_by_Ck(data_set, Ck, min_support, support_data):
    """
    Generate Lk by executing a delete policy from Ck.
    Args:
        data_set: A list of transactions. Each transaction contains several items.
        Ck: A set which contains all all frequent candidate k-itemsets.
        min_support: The minimum support.
        support_data: A dictionary. The key is frequent itemset and the value is support.
    Returns:
        Lk: A set which contains all all frequent k-itemsets.
通过从Ck执行delete策略生成Lk。
参数：
data_set：事务列表。每个事务都包含若干项。
Ck：包含所有频繁候选k项集的集合。
min_support：最小支持。
support_data：字典。键是frequency itemset，值是support。
返回：
Lk：包含所有频繁k项集的集合。
    """
    Lk = set()
    item_count = {}
    for t in data_set:
        for item in Ck:
            if item.issubset(t):
                if item not in item_count:
                    item_count[item] = 1
                else:
                    item_count[item] += 1
    t_num = float(len(data_set))
    for item in item_count:
        if (item_count[item] / t_num) >= min_support:
            Lk.add(item)
            support_data[item] = item_count[item] / t_num
    return Lk


def generate_L(data_set, k, min_support):
    """
    Generate all frequent itemsets.
    Args:
        data_set: A list of transactions. Each transaction contains several items.
        k: Maximum number of items for all frequent itemsets.
        min_support: The minimum support.
    Returns:
        L: The list of Lk.
        support_data: A dictionary. The key is frequent itemset and the value is support.
生成所有频繁项集。
参数：
data_set：事务列表。每个事务都包含若干项。
k： 所有频繁项集的最大项数。
min_support：最小支持。
返回：
L： Lk列表。
support_data：字典。键是frequency itemset，值是support。
    """
    support_data = {}
    C1 = create_C1(data_set)
    L1 = generate_Lk_by_Ck(data_set, C1, min_support, support_data)
    Lksub1 = L1.copy()
    L = []
    L.append(Lksub1)
    for i in range(2, k + 1):
        Ci = create_Ck(Lksub1, i)
        Li = generate_Lk_by_Ck(data_set, Ci, min_support, support_data)
        Lksub1 = Li.copy()
        L.append(Lksub1)
    return L, support_data


def generate_big_rules(L, support_data, min_conf):
    """
    Generate big rules from frequent itemsets.
    Args:
        L: The list of Lk.
        support_data: A dictionary. The key is frequent itemset and the value is support.
        min_conf: Minimal confidence.
    Returns:
        big_rule_list: A list which contains all big rules. Each big rule is represented
                       as a 3-tuple.
从频繁项集生成大规则。
参数：
L： Lk列表。
support_data：字典。键是frequency itemset，值是support。
min_conf：最小信心。
返回：
big_rule_list：包含所有大规则的列表。每个大规则都表示为3元组。
    """
    big_rule_list = []
    sub_set_list = []
    for i in range(0, len(L)):
        for freq_set in L[i]:
            for sub_set in sub_set_list:
                if sub_set.issubset(freq_set):
                    conf = support_data[freq_set] / support_data[freq_set - sub_set]
                    big_rule = (freq_set - sub_set, sub_set, conf)
                    if conf >= min_conf and big_rule not in big_rule_list:
                        # print freq_set-sub_set, " => ", sub_set, "conf: ", conf
                        big_rule_list.append(big_rule)
            sub_set_list.append(freq_set)
    return big_rule_list

def load_data_set():
    """
    Load a sample data set (From Data Mining: Concepts and Techniques, 3th Edition)
    Returns:
        A data set: A list of transactions. Each transaction contains several items.
    """
    data_set = []
    with open('result\\37voxel_set_after_pca-rs.txt', 'r') as file:  # 所有voxel中显著的SNP集合
        data = file.read().split(':')
        for i in range(len(data)-1):
            data1 = data[i].strip(',').split(',')
            data_set.append(data1)

    return data_set

if __name__ == "__main__":
    """
    Test
    """
    import time

    data_set = load_data_set()

    # test_para = numpy.zeros((15, 3))
    # i=0
    # for min_support in numpy.arange(0.4, 0.81, 0.05):
    #     start = time.time()
    #     L, support_data = generate_L(data_set, k=6, min_support = min_support)
    #     total_time = time.time() - start
    #     test_para[i,] = [min_support, total_time, len(support_data)]
    #     i = i+1
    #     print(i, total_time)
    #
    # numpy.savetxt("result/para_time_apriori38.csv",test_para, fmt="%.2f", delimiter=',')

    start = time.time()
    L, support_data = generate_L(data_set, k=4, min_support=0.5)
    print(time.time() - start, 'sec')
    support_data_sort = sorted(support_data.items(), key=lambda item: item[1], reverse=True)
    # for x,v in support_data_sort:
    #     print(x, v)

    for Lk in L:
        print("=" * 50)
        print("frequent " + str(len(list(Lk)[0])) + "-itemsets\t\tsupport")
        print("=" * 50, len(Lk))
        for freq_set in Lk:
            print(freq_set, support_data[freq_set])
    print('')
    # big_rules_list = generate_big_rules(L, support_data, min_conf=0.5)
    # big_rules_list_sort = sorted(big_rules_list, key=lambda item: item[2], reverse=True)
    # print("Big Rules")
    # for item in big_rules_list_sort:
    #     print(item[0], "=>", item[1], "conf: ", item[2])
