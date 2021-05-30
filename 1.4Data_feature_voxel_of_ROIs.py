# Date:2020.09
# Author:Gao Yue

# Function:this script is to get R^2 rank 20% voxel of every ROIs(stand for a  specific ROI)

import nibabel as nib
import numpy as np


# import os


def snp_roi_r2(index):
    snp_voxel = []
    outPath = 'D:\\AllCodes\\Pycharm\\SNP_Correlation\\result\\116ROIs\\'
    filename = '#' + str(index) + '.txt'
    with open(outPath + filename, 'r') as rp:
        index1 = rp.read()
        index2 = index1.split(",")
    indexpath = 'D:\\AllCodes\\Pycharm\\SNP_Correlation\\result\\1784R2\\'
    for i in range(1, 1785):  # 1785,?????????????????????????? change to a specific SNP's R2 file
        indexname = '#' + str(i) + 'SNP.nii.gz'
        img1 = nib.load(indexpath + indexname)
        snpdata1 = img1.get_fdata()
        snpdata = np.reshape(snpdata1, (271633, 1))
        for key in range(len(index2) - 1):
            j = index2[key]
            j = int(j)
            r2 = snpdata[j]
            snp_voxel.append(r2)
    # print("1")
    with open("D:\\AllCodes\\Pycharm\\SNP_Correlation\\result\\1784R2-\\#" + str(index) + "snp_voxel_R2.txt",
              "w") as file:
        for i in range(len(snp_voxel)):
            s = str(snp_voxel[i]).replace('[', '').replace(']', '')
            s2 = s + ","
            #  s = s.replace("'",'').replace(',','')
            file.write(s2)
            # file.close()
        print(str(len(snp_voxel))+'-->'+str(index))


for index in range(1, 117):
    snp_roi_r2(index)
