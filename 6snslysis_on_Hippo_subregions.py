# @Time : 2021/10/30

# @Author : Larry, LuolongCao@163.com

# @File :

# @Software: PyCharm

# -*- coding: utf-8 -*-

import os
import math
import numpy as np
import pandas as pd
import importlib
import nibabel as nib
import neurosynth as ns
from neurosynth.analysis import meta, decode
from scipy.ndimage import zoom
from collections import Counter

dir_name = os.path.dirname(os.path.abspath('.'))
# dir_result = os.path.join(dir_name, '\\tool')
ni1 = os.path.join('D:\\202010LWJ_1515image\\Hippo_12subregions.nii.gz')  # AAL of Hippo subregions
img = nib.load(ni1)
affine = img.affine
mask = np.array(img.get_fdata())
# mask_loc = np.nonzero(mask)
# img_p = np.array(mask.get_fdata()).reshape(-1)
# subregion_info = Counter(img_p)  # 调用Counter函数,查看模板中子区分布情况
# print('Counter(img_p)\n', subregion_info)
# for key, values in subregion_info.items():
#     print(key, values)

#  in whole brain: loc(rs10498633)=1328, loc(rs10277969)=934,loc(rs1047389)=307,loc(rs11731587)=305,loc(rs2242065)=1370
figID = '#1328SNP.nii.gz'; fig_num = 1328;
pathway_in_p = 'F:\\AllCodes\\Pycharm\\SNP_Correlation\\result\\1784P\\'
pathway_in_r2 = np.load('D:\\202106paperLWJvoxel\\1784SNP_R2\\1784SNP_R2.npy')
all_img_r2 = np.zeros((271633,1784))
for rows in range(0,pathway_in_r2.shape[0]):
    all_img_r2[int(pathway_in_r2[rows,1784]-1),] = pathway_in_r2[rows, 0:-1]

pathway_out = 'F:\\AllCodes\\Pycharm\\SNP_Correlation\\result_Hippo_subregion\\'
ni1 = os.path.join(pathway_in_p, figID)  # pathway,
fig_img = nib.load(ni1)
affine = fig_img.affine
fig_img_p = fig_img.get_fdata()
fig_img_r2 = np.array(all_img_r2[:,fig_num]).reshape(mask.shape)
for keys, values in Counter(mask.reshape(-1)).items():
    fig_new = np.zeros((values,2))
    mask_loc = np.where(mask == keys)
    fig_new[:,0] = fig_img_p[mask_loc]
    fig_new[:,1] = fig_img_r2[mask_loc]
    fig_new = fig_new[fig_new[:,1].argsort()[::-1],]    #按第2列，降序排列
    np.savetxt(os.path.join(pathway_out,str(fig_num)+'#'+str(keys)+'.txt'),fig_new[0:math.ceil((fig_new.shape[0])*0.25),:])

    # fig_new.max()
    # newimg = nib.Nifti1Image(fig_new, affine)
    # filename = 'hipp_subregions#' + str(keys) + figID
    # ni2 = os.path.join(pathway_out, filename)
    # nib.save(newimg, ni2)
