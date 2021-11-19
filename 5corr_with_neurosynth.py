# @Time : 2021/10/7

# @Author : Larry

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
# ns.dataset.download(path='.', unpack=True)

from neurosynth.base.dataset import Dataset
dataset = Dataset('data/database.txt')
dataset.add_features('data/features.txt')   # this required the pandas hava "to_dense()" attribution, such as 0.25.0
# dataset.get_feature_names()   # dataset.masker.dims=(91, 109, 91)
ids = dataset.get_studies(features='emo*', frequency_threshold=0.05)
# len(ids)  # 2191

ma = meta.MetaAnalysis(dataset, ids)
ma.save_results('some_directory/emotion')

# resize your own image in to dim=(91, 109, 91)
#  in whole brain: loc(rs10498633)=1328, loc(rs10277969)=934,loc(rs1047389)=307,loc(rs11731587)=305,loc(rs2242065)=1370
pathway_in = 'D:\\AllCodes\\Pycharm\\SNP_Correlation\\result\\1784P\\'
pathway_out = 'D:\\AllCodes\\Pycharm\\SNP_Correlation\\'
fid = '1328'
ni1 = os.path.join(pathway_in, '#1328SNP.nii.gz')  # pathway,
img = nib.load(ni1)
affine = img.affine
img_p = img.get_fdata()
img_p_new = zoom(img_p, (91/61, 109/73, 91/61)) # do interpolation by scipy
newimg = nib.Nifti1Image(img_p_new, affine)
filename = 'interp#' + str(fid) + 'SNP.nii.gz'
ni2 = os.path.join(pathway_out, filename)
nib.save(newimg, ni2)

# Decode your own images
decoder = decode.Decoder(dataset, features=['taste', 'disgust', 'emotion', 'auditory', 'pain', 'somatosensory', 'conflict', 'switching', 'inhibition'])
# data = decoder.decode(['pIns.nii.gz', 'vIns.nii.gz', 'dIns.nii.gz'], save='decoding_results.txt')
data = decoder.decode(['F:\\AllCodes\\Pycharm\\SNP_Correlation\\interp#1328SNP.nii.gz'], save = 'F:\\AllCodes\\Pycharm\\SNP_Correlation\\decoding_results.txt')