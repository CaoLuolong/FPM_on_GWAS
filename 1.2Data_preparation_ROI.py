# Date:2020.09
# Author:Gao Yue

# Function:this script is to do preparation of ROIs(transfer from 3d to 1d, extract 116 ROIs' index).

import nibabel as nib
import numpy as np


# import os


def myfind(index, value):
    index_list = []
    for k in range(len(value)):
        if value[k] == index:
            index_list.append(k)
            fileName = '#' + str(index) + '.txt'
            with open(filepath_out + fileName, 'w') as f:
                # if i == len(b):
                for i in range(len(index_list)):
                    s = str(index_list[i]) + ","
                    f.write(s)

    # print(b)


filepath_out = 'D:\\AllCodes\\Pycharm\\SNP_Correlation\\result\\116ROIs\\'
img1 = nib.load('D:\\AllCodes\\Pycharm\\SNP_Correlation\\rawdata\\atlas116--.nii')
roidata1 = img1.get_fdata()
roidata = np.reshape(roidata1, (271633, 1))  # 271633
for i in range(1, 117):
    myfind(i, roidata)
