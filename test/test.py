#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
@File    :   test.py
@Time    :   2020/12/10 15:56:27
@Author  :   liangpingguo 
@Version :   1.0
@Contact :   864695417@qq.com
@Blog 	  :   https://blog.csdn.net/liangpingguo
@Desc    : 老板你再这样我要删库了
'''
# Start typing your code from here
import  os
import shutil

# print (os.getcwd()) #获取当前工作目录路径
# print (os.path.abspath('.')) #获取当前工作目录路径
# print (os.path.abspath('test.txt')) #获取当前目录文件下的工作目录路径
# print (os.path.abspath('..')) #获取当前工作的父目录 ！注意是父目录路径
# print (os.path.abspath(os.curdir)) #获取当前工作目录路径


# 判断文件是否存在
def fileExists(filename):
    if os.path.exists(filename):
        return True
    else:
        return False

 # 读txt文件
def readtxt(filename,resultList):
    print(filename)
    # 加上编码UTF-8是为了处理中文字符，否则如果读取到中文字符会抛出异常
    f=open(filename,'r',encoding='UTF-8')
    # readlines一次读取文本所有字符，返回结果是列表，并且包含换行符
    str=f.readlines()
    listlen=len(str)

    # 处理换行符
    for i in range(listlen):
        temp=str[i]
        if i==listlen-1:
            resultList.append(temp)
        else:
            # 分割换行符
            a=temp.split('\n')
            resultList.append(a[0])
    f.close()

# 写入txt文件
def writeTxt(filename,str):
    f = open(filename, 'r+',encoding='UTF-8')
    # read()方法的作用就是将文件指针置位最后，否则文件指针在开头，将会覆盖文件原有内容
    f.read()
    # write方法不会添加换行符，所以需要手动增加换行符
    f.write('\n'+str)
    f.close()

 

def deletefile(filename):
    if (fileExists(filename)):
        os.remove(filename)
        return True
    else:
        return False
 
if __name__ == "__main__":
    filename='D:\\project\\kjyw-py\\config.txt'

    resultList=[]
    if ( fileExists(filename)):
        readtxt(filename,resultList)
        print(resultList)
        writeTxt(filename, 'helloWorld')
