# -*- encoding: utf-8 -*-
'''
@File    :   mas_flow_merge.py
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
import datetime

curdir = os.path.abspath(os.path.dirname(__file__))  # 当前目录
mas_file_full_name='MASLIST20210223.xlsx'
jk_file_full_name = 'MASJK01_RESULT_202101.txt'  # 接口流量文件全名，有后缀

jk_file_name = os.path.splitext(jk_file_full_name)[0]  # 接口流量文件名，无后缀
flow_name = 'F_' + jk_file_name.split('_')[-1]  #截取接口文件年月做流量标题

jk_file_path_old = curdir + os.sep + jk_file_full_name #接口流量原文件路径
jk_file_path_new = curdir + os.sep + jk_file_name + ".xlsx"  #格式化,并转为xlsx后的接口流量路径
mas_file_path = curdir + os.sep + mas_file_full_name  #MAS 清单路径

#读取接口流量数据,只保留列：["短信接入号","流量"]，注意接入号需转为字符串
data_jk = pd.read_csv(jk_file_path_old,encoding='gbk',dtype=str).iloc[:, [9, 17]]
#接口流量数据格式化，添加标题行：["短信接入号", "流量"]
data_jk_frame = pd.DataFrame(data_jk.values, columns=["短信接入号", flow_name])
# 保存为新的接口流量表：
data_jk_frame.to_excel(jk_file_path_new, encoding='utf-8', index=False)

data_mas = pd.read_excel(mas_file_path)#读取MAS清单
data_jk = pd.read_excel(jk_file_path_new)  #读取接口流量
# 数字转化为字符串
data_mas['集团编号'] = data_mas['集团编号'].astype(str)
data_mas['短信接入号'] = data_mas['短信接入号'].astype(str)
data_jk['短信接入号'] = data_jk['短信接入号'].astype(str)

#mas清单和接口流量两表使用左连接查询，即保留左表MAS清单，联查条件：短信接入号
data_mas_flow = pd.merge(data_mas, data_jk, how='left', on='短信接入号')
# print(data_mas_flow.head())
#指定保留列
# maslist_result = data_mas_flow.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]]
# print(maslist_result.head())

data_mas_flow.to_excel(curdir + os.sep + 'MAS_FLOW_LIST_RESULT_'+datetime.datetime.now().strftime('%Y%m%d')+'.xlsx',
                        index=False,
                        header=True)

