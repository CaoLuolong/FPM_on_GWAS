# Date:2020.09
# Author:Gao Yue

# Function:this script is to generate a compound SNP(include pvalue)
import numpy as np

newsnp = np.zeros((49900, 3), dtype=np.double)
newSNP = np.zeros((49900, 2), dtype=np.double)
count = 0

# get the minimum pvalue of a voxel in SNP-sets as the terminal p
for index in (1781, 1770, 1772):
    filepath = 'D:\\AllCodes\\Pycharm\\SNP_Correlation\\result\\SNPs-ROIs\\'
    filename = '#' + str(index) + 'snp_voxel_pvalue.txt'
    with open(filepath + filename, "r") as file:
        content1 = file.read().split(",")
        for i in range(len(content1) - 1):
            newsnp[i, count] = float(content1[i])
    count += 1

for i in range(len(content1) - 1):
    newSNP[i, 0] = i + 1
    newSNP[i, 1] = min(newsnp[i,])



