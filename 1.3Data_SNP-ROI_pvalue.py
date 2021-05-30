# Date:2020.09
# Author:Gao Yue

# Function:this script is to do preparation of SNPs(get p value of 1784SNIPs in all 116ROIs)

import nibabel as nib
import numpy as np


# import os


def snp_roi(index):
    snp_voxel = []
    roiPath = 'D:\\AllCodes\\Pycharm\\SNP_Correlation\\result\\116ROIs\\'
    indexpath = 'D:\\AllCodes\\Pycharm\\SNP_Correlation\\result\\1784P\\'
    indexname = '#' + str(index) + 'SNP.nii.gz'
    img1 = nib.load(indexpath + indexname)
    snpdata1 = img1.get_fdata()
    snpdata = np.reshape(snpdata1, (271633, 1))

    for i in range(1, 117):
        fileName = '#' + str(i) + '.txt'
        with open(roiPath + fileName, 'r') as rp:
            index1 = rp.read()
            index2 = index1.split(",")
            for i in range(len(index2) - 1):
                j = index2[i]
                j = int(j)
                k = snpdata[j]
                pvalue = 10 ** (-k)
                snp_voxel.append(pvalue)
    # print("1")
    with open("D:\\AllCodes\\Pycharm\\SNP_Correlation\\result\\SNPs-ROIs\\#" + str(index) + "snp_voxel_pvalue.txt",
              "w") as file:
        for i in range(len(snp_voxel)):
            s = str(snp_voxel[i]).replace('[', '').replace(']', '')
            s2 = s + ","
            #  s = s.replace("'",'').replace(',','')
            file.write(s2)
            # file.close()
    print(str(len(snp_voxel))+'-->'+str(index))


for index in range(1, 1785):
    snp_roi(index)
