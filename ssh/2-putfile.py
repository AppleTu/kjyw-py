# -*- coding: utf-8 -*-
# @Time    : 2020/3/30 9:51
# @Author  : lp
# @desc    : 老板你再这样我要删库了
'''
1.配置文件：config.txt
2.根据配置文件上传文件至远端服务器指定目录
'''
import os
import pandas as pd

import Server


conf_file = #'E:\\0yunmasfile\\yunmas-jiaoben\\1-putfile-pro-o.txt' # 本地配置文件
conf_file=os.path.abspath('config.txt') #获取本地配置文件,当前目录文件下的工作目录路径
local_dir='E:\\0yunmasfile\\yunmas-jiaoben'  # 本地文件存放目录：比如tomcat、war等
remote_dir='/home/yunmas'           # 远端服务器应用存放目录
remote_bak_dir = '/home/yunmas/dbbak'       # 远端服务器应用备份目录

# 读取本地配置文件
pd.read_csv(conf_file, sep=' ')
hostList = pd.read_table(conf_file, encoding='gb2312', delim_whitespace=True, index_col=0)
for index, row in hostList.iterrows():
    print(index)
    # print("ip:" + row["ip"], "uname:" + row["uname"], "pwd:" + row["pwd"], "from:" + row["from"], "to:" + row["to"], "bakdir:" + row["bakdir"])  # 输出各列
    ip=row["ip"]
    username=str(row["uname"])
    password=str(row["pwd"])
    filename=str(row["filename"])
    localfile=str(local_dir+os.sep+filename)
    remotefile=str(remote_dir+'/'+filename)
    remotebakfile=str(remote_bak_dir+'/'+filename)

    s=Server.Server(ip,22,username,password) # 实例化
    check=s.exists_local(localfile) # 检查本地路径文件是否存在
    if check==True: # 如果存在，继续
        try:
            print(s.connect())      # 创建一个连接
            print(s.open_ssh())     # 开启ssh
            print(s.open_sftp())  # 开启sftp
            print(s.mv_remote(remotefile,remotebakfile)) # 原文件至dbbak
            print(s.sftp_put(localfile,remotefile)) # 上传文件

        except Exception as _e:
            print( '异常：%s' % _e)
        finally:
            if s:
                print(s.close())
                del s
    else: # 如果不存在，返回错误信息
        print(check)
