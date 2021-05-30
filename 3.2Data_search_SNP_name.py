# Date:2020.09
# Author:Gao Yue

# Function:this script is to do preparation of SNPs(extract 1784 SNPs' features)

def main():
    def snp(i):
        snp_list = []
        with open("D:\\AllCodes\\Pycharm\\SNP_Correlation\\rawdata\\snp1784.txt") as file:
            f = file.readlines()
            # print(len(f))    结果是1784
            for snp in range(len(f)):
                snp_list.append(f[snp])
        print(snp_list[i - 1])

    snp(688)


if __name__ == "__main__":
    main()