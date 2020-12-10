#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
@File    :   test2.py
@Time    :   2020/12/10 17:24:25
@Author  :   liangpingguo 
@Version :   1.0
@Contact :   864695417@qq.com
@Blog 	  :   https://blog.csdn.net/liangpingguo
@Desc    : 老板你再这样我要删库了
'''
# Start typing your code from here
with open ("D:\\project\\kjyw-py\\config.txt") as file_object:
    contents = file_object.read()
    print(contents.strip())
