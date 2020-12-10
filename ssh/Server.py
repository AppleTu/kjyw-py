#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
@File    :   Server.py
@Time    :   2020/12/10 16:23:11
@Author  :   liangpingguo 
@Version :   1.0
@Contact :   864695417@qq.com
@Blog 	  :   https://blog.csdn.net/liangpingguo
@Desc    : 老板你再这样我要删库了
'''
# Start typing your code from here

import os
import time

import paramiko
from time import sleep

import pandas as pd


class Server(object):
    """
    构建一个公共服务类
    这里说明一下：
    远端服务器为 linux
    本地服务器为 windows ,运行本脚本的服务器
    """
    def __init__(self, ip='', port=22, username='', password='', timeout=30):
        """
        通过IP, 端口，用户名，密码，超时时间，初始化一个远程主机
        :param str ip:
        :param int port: default value is 22
        :param str username:
        :param str password:
        :param int timeout: default value is 30.
        """
        # 连接信息
        self._ip = ip
        self._port = port
        self._username = username
        self._password = password
        self._timeout = timeout
        # transport, channel, ssh, sftp, prompt
        self._transport = None
        self._channel = None
        self._ssh = None
        self._sftp = None
        self._prompt = None
        # 连接失败的重试次数（总计3次尝试）
        self._try_times = 2

    # 调用connect方法连接远程主机
    def connect(self):
        """
        :return: result
        """
        _result = ''
        while True:
            # 尝试连接
            try:
                # 创建一个通道
                self._transport = paramiko.Transport((self._ip, self._port))
                self._transport.connect(username=self._username, password=self._password)
                # 如果没有抛出异常说明连接成功，直接返回
                _result += '%s con 创建成功' % self._ip
                break
            # 这里对可能的异常如网络不通、链接超时、socket.error, socket.timeout直接输出
            except Exception as _e:
                if self._try_times != 0:
                    _result += '第%i次连接 %s 异常，原因：%s\n' % (3 - self._try_times, self._ip, _e)
                    _result += '进行重试\n'
                    self._try_times -= 1
                else:
                    _result += '第%i次连接 %s 异常，原因：%s\n' % (3 - self._try_times, self._ip, _e)
                    _result += '连接远程主机 %s 失败，结束重试' % self._ip
                    break
        return _result

    # 开启ssh
    def open_ssh(self):
        # 连接ssh
        try:
            # 实例化SSHClient
            self._ssh = paramiko.SSHClient()
            # 这行一定要呀  大概是允许连接不在know_hosts文件中的主机 # 设置新主机和密码管理策略, 接受一个参数, 值可以是 AutoAddPolicy、RejectPolicy、WarningPolicy, 默认为 RejectPolicy
            self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._ssh._transport = self._transport
            return '%s ssh 连接成功' % self._ip
        except Exception as _e:
            return '%s ssh 连接异常：%s' % (self._ip, _e)

    # ssh发送无需交互的单条命令
    def ssh_send_cmd(self, cmd):
        """
        仅支持无需交互的指令
        :param str cmd:
        :return: str stdout、str stderr
        """
        try:
            _stdin, _stdout, _stderr = self._ssh.exec_command(cmd)
            # 返回decode的指令stdout和stderr信息
            str_out = _stdout.read().decode()
            str_err = _stdout.read().decode()
            if str_err != "":
                print(str_err)
            return str_out
        except Exception as _e:
            return 'ssh指令执行异常：%s' % _e

    # 检查远程服务器上文件是否存在
    def exists_remote(self, remotefile):
        """
        检查远程服务器上的文件是否存在
        :param remotefile: 远端的绝对路径+文件名
        :return: ls 目录检查的正确结果
        """
        try:
            cmd='ls '+ remotefile
            _stdin, _stdout, _stderr = self._ssh.exec_command(cmd)
            # 返回decode的指令stdout和stderr信息
            return _stdout.read().decode()
        except Exception as _e:
            return '"%s" 指令执行异常：%s' % (cmd,_e)

    # 检查本地服务器上文件是否存在
    def exists_local(self,localfile):
        """
        检查本地服务器上的文件是否存在
        :param localfile: 本地的绝对路径+文件名
        :return: 检查结果
        """
        if not os.path.exists(localfile ):
            return '检查本地文件路径不通过：%s 目录或文件不存在' % localfile
        else:
            return True

    # mv 远程服务器上文件至指定目录
    def mv_remote(self,originalFile, targetFile):
        """
        备份原文件
        :param OriginalFile: 远端的绝对路径+文件名
        :param targetFile: 远端的备份路径+文件名+时间戳
        :return: mv 命令执行的正确结果
        """
        try:
            cmd ='mv '+ originalFile +' ' +targetFile+'.bak-'+self.get_current_time()
            if self.exists_remote(originalFile)=="":
                return '"%s" 指令未执行：原文件不存在！' % cmd
            else:
                _stdin, _stdout, _stderr = self._ssh.exec_command(cmd)
                # 返回decode的指令stdout和stderr信息
                r=_stdout.read().decode()
                if r=="":
                    return '"%s" 指令执行成功' % cmd
                else:
                    return '"%s" 指令执行失败：%s' % (cmd, r)
        except Exception as _e:
            return '"%s" 指令执行异常：%s' % (cmd, _e)

    # 开启sftp
    def open_sftp(self):
        # 连接sftp
        try:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
            return '%s sftp 连接成功' % self._ip
        except Exception as _e:
            return '%s sftp 连接异常：%s' % (self._ip, _e)

    # sftp get单个文件
    def sftp_get(self, remotefile='', localfile=''):
        """
        :param str remotefile: 远端的绝对路径+文件名
        :param str localfile: 本地的绝对路径+文件名
        :return: 下载结果
        """
        try:
            self._sftp.get(remotefile, localfile)
            return '%s 下载成功' % remotefile
        except Exception as e:
            return '%s 下载异常：%s' % (remotefile, e)

    # sftp put单个文件
    def sftp_put(self, localfile='', remotefile=''):
        """
        :param str localfile: 本地的绝对路径+文件名
        :param str remotefile: 远端的绝对路径+文件名
        :return: 上传结果
        """
        try:
            self._sftp.put(localfile, remotefile)
            return '✔ 上传成功:%s to %s ' % (localfile,remotefile)
        except Exception as e:
            return '✘ 上传异常(%s )：%s' % (localfile, e)

    # 开启channel
    def open_channel(self):
        """
        :return: result
        """
        _result = ''
        try:
            self._channel = self._transport.open_session()
            self._channel.settimeout(self._timeout)
            self._channel.get_pty()
            self._channel.invoke_shell()
            # 如果没有抛出异常说明连接成功
            _result += '%s channel 建立成功' % self._ip
            sleep(1)  # 等待1秒，接收SSH banner信息
            _Banner = self._channel.recv(65535)  # 接收ssh banner信息
        except Exception as _e:
            _result += '%s channel 建立异常：%s' % (self._ip, _e)
        return _result

    # 获取channel提示符
    def get_prompt(self, expect_symbol=''):
        """
        :param str expect_symbol: The prompt's symbol,like '>','# ','$ ',etc.
        :return: result
        """
        _result = ''
        try:
            # 发送"Enter"获取提示符
            n = 0
            while n < 3:
                self._channel.send("\r")
                # 暂停0.5~1秒接收输入回车后的返回结果
                sleep(0.5)
                _Prompt_vendor = self._channel.recv(64)
                # 获取提示符的两种方式：
                # 1. 按\r\n进行字符串分割，后边的就是完整的提示符
                self._prompt = _Prompt_vendor.decode('utf-8').split('\r\n')[-1]
                # 2. 提示符取输出的后x位，即_Prompt_vendor[-x:]
                # self._prompt = _Prompt_vendor[-2:].decode('utf-8')
                # 如果获取的提示符由期待的提示符末尾标识符结尾，判断为获取成功
                if self._prompt.endswith(expect_symbol):
                    _result += '提示符获取成功(%s)' % self._prompt
                    break
                n += 1
            else:
                _result += '提示符获取异常(%s)' % self._prompt
        except Exception as _e:
            _result += '提示符获取异常：%s' % _e
        return _result

    # 通过channel发送指令，返回执行结果。如果指令是交互指令，则需要给出交互的断点提示符
    def channel_send_cmd(self, cmd='', break_prompt=''):
        """
        通过channel发送指令。
        如果是交互式指令，必须要给出break_prompt！用来判断断点，结束while循环，返回结果
        无需交互的指令，break_prompt空着就行
        :param str cmd: 执行的指令，支持交互指令
        :param str break_prompt: 判断指令结束/断点的提示符。默认为channel的提示符
        :return: result
        """
        _stream = ''
        if not break_prompt:
            break_prompt = self._prompt
        try:
            cmd += '\r'
            # 通过提示符来判断命令是否执行完成
            # 发送要执行的命令
            self._channel.send(cmd)
            # 回显很长的命令可能执行较久，通过循环分批次取回回显
            while True:
                sleep(0.5)
                _stream += self._channel.recv(1024).decode('utf-8')
                if _stream.endswith(break_prompt):
                    break
            return _stream
        except Exception as _e:
            return 'channel执行指令异常：%s' % _e

    # 释放资源
    def close(self):
        # 断开连接
        if self._ssh:
            self._ssh.close()
        if self._channel:
            self._channel.close()
        if self._transport:
            self._transport.close()
        return '%s 连接已关闭' % self._ip

    def __del__(self):
        return

    # 获取时间戳
    def get_current_time(self):
        """
        获取当前时间时间戳
        :return: 格式化后的时间戳
        """
        t=time.time()
        t_format=time.strftime('%Y-%m-%d-%H%M%S ',time.localtime(time.time()))
        return t_format


if __name__ == '__main__':
    conf_file = 'E:\\0yunmasfile\\yunmas_jiaoben\\1-putfile.txt'
    local_dir='E:\\0yunmasfile\\yunmas-latest'
    remote_dir='/home/yunmas/appBase'
    remote_bak_dir = '/home/yunmas/dbbak'

    # 读取本地配置文件
    pd.read_csv(conf_file, sep=' ')
    hostList = pd.read_table(conf_file, encoding='gb2312', delim_whitespace=True, index_col=0)
    for index, row in hostList.iterrows():
        print(index)
        # print("ip:" + row["ip"], "uname:" + row["uname"], "pwd:" + row["pwd"], "filename:" + row["filename"])  # 输出各列
        ip=row["ip"]
        username=str(row["uname"])
        password=str(row["pwd"])
        filename=str(row["filename"])
        localfile=str(local_dir+os.sep+filename)
        remotefile=str(remote_dir+'/'+filename)
        remotebakfile=str(remote_bak_dir+'/'+filename)

        s=Server(ip,22,username,password) # 实例化
        check=s.exists_local(localfile) # 检查本地路径文件是否存在
        if check==True: # 如果存在，继续
            try:
                print(s.connect())      # 创建一个连接
                print(s.open_ssh())     # 开启ssh
                print(s.open_sftp())  # 开启sftp
                # print(s.mv_remote(remotefile,remotebakfile)) # 原文件至dbbak
                # print(s.sftp_put(localfile,remotefile)) # 上传文件

                # ssh发送无交互的指令
                print(s.ssh_send_cmd('ls /home/yunmas'))
                print('- - - - - - - - - - - -')
                # 使用channel发送交互指令
                print(s.open_channel())
                print(s.get_prompt(expect_symbol='# '))
                print(s.channel_send_cmd('df'))

            except Exception as _e:
                print( '异常：%s' % _e)
            finally:
                if s:
                    print(s.close())
                    del s
        else: # 如果不存在，返回错误信息
            print(check)




