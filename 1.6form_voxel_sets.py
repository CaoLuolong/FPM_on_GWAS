# @Time : 2020/12/3 14:43 

# @Author : Larry

# @File : 1.6form_voxel_sets.py : form 49900 sets, each contain significant SNP indexes.

# @Software: PyCharm

import os
import math
import time  # 时间函数
import numpy as np
import nibabel as nib
start = time.perf_counter()

filepath_out = 'D:\\AllCodes\\Pycharm\\SNP_Correlation\\result\\'
img1 = nib.load('D:\\AllCodes\\Pycharm\\SNP_Correlation\\rawdata\\atlas116--.nii')
roidata1 = img1.get_fdata()
roidata = np.reshape(roidata1, (271633, 1))  # 271633

count = 0
index_list = []
for k in range(len(roidata)):
    if (roidata[k] in range(1, 117)):
        index_list.append(k)
        count += 1
print(count)

snpnum = 1784# 500
snpdata = np.zeros((271633, snpnum))
for index in range(1, snpnum + 1):
    indexpath = 'D:\\AllCodes\\Pycharm\\SNP_Correlation\\result\\1784P\\'
    indexname = '#' + str(index) + 'SNP.nii.gz'
    img1 = nib.load(indexpath + indexname)
    snpdata1 = img1.get_fdata()
    snpdata[:, index - 1] = np.reshape(snpdata1, (271633, 1)).reshape(271633, )

fileName = '49900set0.txt'
with open(filepath_out + fileName, 'w') as f:
    for i in index_list:
        set = []
        for j in range(snpnum):
            if (snpdata[i, j] > -math.log10(0.05)): set.append(j + 1)
        f.write(','.join(str(s) for s in set))
        f.write(':')

f.close()

elapsed = (time.perf_counter() - start)
print("Time used:",elapsed)
