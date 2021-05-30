# Date:2020.09
# Author:Gao Yue

# Function:this script is to do count the num of significant pvalue of voxel in SNPs and sort them

# import nibabel as nib
# import numpy as np
import itertools
# import os


def sort_desc():
    p = 0.005
    # count = 0
    sort1 = []
    for index in range(1, 1785):
        count = 0
        #        sort1 = []
        filepath = 'D:\\AllCodes\\Pycharm\\SNP_Correlation\\result\\SNPs-ROIs\\'
        filename = '#' + str(index) + 'snp_voxel_pvalue.txt'
        with open(filepath + filename, "r") as file:
            content2 = file.read()
            content1 = content2.split(",")
            for i in range(len(content1) - 1):
                aa = content1[i]
                bb = float(aa)
                if bb < p:  # 判断符合p<0.005的个数放入count
                    count += 1
            sort1.append(count)
        # 将sort1添加键值（即snp序号）并且将sort1由列表变为字典
    keys = []
    for keyi in range(1, 1785):
        keys.append(keyi)
    snp_p_num = (itertools.zip_longest(keys, sort1))
    desc_sorted = sorted(snp_p_num, reverse=True, key=lambda x: x[1])

    with open("result\\psort_SNP.txt", "w") as file:
        for i in range(1, 1784):
            s = str(desc_sorted[i])
            s1 = s + ","
            file.write(s1)


sort_desc()
# for index in range(1,1785):
#    sort_desc(index)
