# -*- coding: utf-8 -*-
# @Time    : 2020/3/30 9:51
# @Author  : lp
# @desc    : 老板你再这样我要删库了
'''
1.配置文件：1-putfile.txt
2.根据配置文件上传文件至远端服务器指定目录
'''
import os
import time
import pandas as pd

import Server

# conf_file = 'D:\\project\\kjyw-py\\ssh\\config.txt'  # 本地配置文件
conf_file = os.path.abspath(
    os.path.dirname(__file__)) + os.sep + 'config.txt'  # 本地配置文件
# 读取本地配置文件
pd.read_csv(conf_file, sep=' ')
hostList = pd.read_table(conf_file,
                         encoding='gb2312',
                         delim_whitespace=True,
                         index_col=0)
for index, row in hostList.iterrows():

    # print("ip:" + row["ip"], "uname:" + row["uname"], "pwd:" + row["pwd"], "from:" + row["from"], "to:" + row["to"], "bakdir:" + row["bakdir"])  # 输出各列
    ip = row["ip"]
    username = str(row["uname"])
    password = str(row["pwd"])
    print(index, row["ip"])

    s = Server.Server(ip, 22, username, password)  # 实例化
    try:
        #print(s.connect())      # 创建一个连接
        #print(s.open_ssh())     # 开启ssh
        #print(s.open_sftp())    # 开启sftp

        s.connect()  # 创建一个连接
        s.open_ssh()  # 开启ssh
        # s.open_sftp()  # 开启sftp
        s.open_channel()

        # ssh发送无交互的指令
        #print(s.ssh_send_cmd('chmod ug+x /home/yunmas/*'))
        #print(s.ssh_send_cmd('rm -rf /home/yunmas/xxxxxxx'))
        #print(s.ssh_send_cmd('/home/yunmas/moni/ping.sh'))
        #print(s.ssh_send_cmd('su - \n'))
        #time.sleep(1)
        print(s.ssh_send_cmd('openssl version'))
        # print(s.ssh_send_cmd('ll /home'))
        # print(s.ssh_send_cmd('/home/yunmas/stop-all.sh'))
        # print(s.ssh_send_cmd('/home/yunmas/start-all.sh'))
        # print(s.ssh_send_cmd('mv /home/yunmas/tomcat /home/yunmas/dbbak/tomcat-bak-20200401'))
        # print(s.ssh_send_cmd('python /home/yunmas/autoDeployTomcat.py'))
        # 使用channel发送交互指令
        # print(s.open_channel())
        #print(s.get_prompt(expect_symbol='$ '))
        #print(s.channel_send_cmd('cat /home/yunmas/moni/pinglog.log'))

    except Exception as _e:
        print('异常：%s' % _e)
    finally:
        if s:
            s.close()
            del s
