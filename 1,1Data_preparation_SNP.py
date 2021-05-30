# Date:2020.09
# Author:Gao Yue

# Function:this script is to do preparation of SNPs(extract 1784 SNPs' features)

import os
import math
import numpy as np
import nibabel as nib

pathway_in = 'D:\\AllCodes\\Pycharm\\SNP_Correlation\\rawdata\\'
pathway_out = 'D:\\AllCodes\\Pycharm\\SNP_Correlation\\result\\1784P\\'
ni1 = os.path.join(pathway_in, 'mri.nii')  # pathway,
img = nib.load(ni1)
affine = img.affine

# ----------------
voxel = os.path.join(pathway_in, 'voxel.txt')
f = open(voxel)
str2 = f.read()
p2 = str2.split(',')  # 271633，非零位点有49900个

for fid in range(1, 1785):  # 1286,1785
    filename = '#' + str(fid) + 'SNP.txt'
    ni2 = os.path.join('E:\\202009GY20.09小论文\\GY_SNP', filename)
    f = open(ni2)
    str1 = f.read()
    # str2 = str1
    p1 = str1.split(',')  # 一个SNP（fid）与所有271633个voxel的相关性p值

    P = np.zeros((61, 73, 61))

    for i in range(61): #消除底片中外围干扰-->64411
        for j in range(73):
            for k in range(61):
                if (float(p2[i + j * 61 + 61 * 73 * k]) > 0.01 and float(p1[i + j * 61 + 61 * 73 * k]) > 0):
                    aa = float(p1[i + j * 61 + 61 * 73 * k])
                    bb = math.log10(aa)
                    P[i][j][k] = 0 - bb
                else:
                    P[i][j][k] = 0

    ##for i in range(271633):
    ##        aa=float(p[i])
    ##        P.append('0')
    ##        P[i]=aa
    ##
    ##P=np.reshape((P),(-1,73,61))
    newimg = nib.Nifti1Image(P, affine)
    filename2 = '#' + str(fid) + 'SNP.nii.gz'
    ni2 = os.path.join(pathway_out, filename2)
    nib.save(newimg, ni2)
