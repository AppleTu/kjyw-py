# -*- encoding: utf-8 -*-
'''
@File    :   toexcel.py
@Time    :   2021/02/23 22:47:45
@Author  :   liangpingguo 
@Version :   1.0
@Contact :   864695417@qq.com
@Blog    :   https://blog.csdn.net/liangpingguo
@Desc    :   老板你再这样我要删库了
'''
# Start typing your code from here
# coding:utf-8

import pandas as pd
import os


def get_path(file_path):
    path_list = []
    xls_list = []
    file_list = os.listdir(file_path)
    file_list.sort(key=lambda x: int(x[:2]))  # 对读取的文件进行排序
    for filename in file_list:
        complete_path = os.path.join(file_path, filename)
        path_list.append(complete_path)
    for path in path_list:
        f = open(path, 'r')
        tr = pd.read_table(f)
        xls_path = 'e:/Project/py/kjyw-py/test/jk2.xls'
        tr.to_excel(xls_path, header=None)
        xls_list.append(xls_path)
    return xls_list


if __name__ == '__main__':
    p = 'E:/Project/py/kjyw-py/test/jk.txt'
    print(get_path(p))
