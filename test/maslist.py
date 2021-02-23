# -*- encoding: utf-8 -*-
'''
@File    :   maslist.py
@Time    :   2021/02/23 19:10:06
@Author  :   liangpingguo 
@Version :   1.0
@Contact :   864695417@qq.com
@Blog    :   https://blog.csdn.net/liangpingguo
@Desc    :   老板你再这样我要删库了
'''
# Start typing your code from here
import numpy as np
import pandas as pd
import os

curdir = os.path.abspath(os.path.dirname(__file__))  # 当前路径
data_jktxt = pd.read_csv(curdir + os.sep + 'jk.txt')
data_jktrani
# data_mas = pd.read_excel(curdir + os.sep + 'MASLIST20210223.xlsx')
# data_jk = pd.read_excel(curdir + os.sep + 'jk.xlsx')
# data_mas['集团编号'] = data_mas['集团编号'].astype(str)
# data_mas['短信接入号'] = data_mas['短信接入号'].astype(str)
# data_jk['短信接入号'] = data_jk['短信接入号'].astype(str)
# data_masflow = pd.merge(data_mas, data_jk, how='left', on='短信接入号')
# maslist_result = data_masflow.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 18]]
# #print(maslist_result)

# maslist_result.to_excel(curdir + os.sep + 'MASLIST_RESULT.xlsx',
#                         index=False,
#                         header=True)
