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
import os
import shutil

print(os.getcwd())  #获取当前工作目录路径
print(os.path.abspath('.'))  #获取当前工作目录路径(绝对路径)
print(os.path.abspath('ssh/config.txt'))  #获取当前目录文件下的工作目录路径
print(os.path.abspath('..'))  #获取当前工作的父目录 ！注意是父目录路径
print(os.path.abspath(os.curdir))  #获取当前工作目录路径
print(os.path.abspath(os.path.dirname(__file__)))  #获取当前工作目录路径
