# -*- coding: utf-8 -*-
# @Time    : 2020/4/9 10:35
# @Author  : lp
# @desc    : 老板你再这样我要删库了
import re
import time
from time import sleep

import pandas as pd
from numpy import long
from pandas.tests.io.excel.test_xlsxwriter import xlsxwriter

import Server

#
def trywexrestr(lists):
    nowtime = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())) + ""
    bookurl = "systemsinfo-" + nowtime + '.xlsx'
    # filenames=nowtime+'info.xlsx'
    workbook1 = xlsxwriter.Workbook(bookurl)
    worksheet = workbook1.add_worksheet()
    title = [u'id', u'IP地址', u'主机名', u'系统版本', u'系统时间', u'系统运行时间', u'可登陆用户数', u'可登陆用户', u'当前用户数' \
        , u'负载', u'CPU使用率', u'内存总量', u'内存使用率', u'swap大小', u'swap使用率', u'根目录大小', u'app大小', u'app使用率' \
        ,u'read/次/秒',u'write/次/秒', u'接收字节数', u'发送字节数', u"本机开放端口",u'备注']
    format = workbook1.add_format()
    worksheet.set_column("A:A", 3)
    worksheet.set_column(1, 19, 15)
    format.set_bold()
    worksheet.write_row('A1', title, format)
    row = 1

    # <editor-fold desc="for 循环输出到sheet">
    for a in lists:
        worksheet.write(row, 0, a["id"])
        worksheet.write(row, 1, a["ip"])
        worksheet.write(row, 2, a["hostname"])
        worksheet.write(row, 3, a["version"])
        worksheet.write(row, 4, a["current_time"])
        worksheet.write(row, 5, a["operation_time"])
        worksheet.write(row, 6, a["can_login_users"])
        worksheet.write(row, 7, a["can_login_user_num"])
        worksheet.write(row, 8, a["current_users"])
        worksheet.write(row, 9, a["load_average"])
        worksheet.write(row, 10, a["cpu_usage"])
        worksheet.write(row, 11, a["momery_total"])
        worksheet.write(row, 12, a["momery_usage"])
        worksheet.write(row, 13, a["swap_total"])
        worksheet.write(row, 14, a["swap_usage"])
        worksheet.write(row, 15, a["disk_all"])
        worksheet.write(row, 16, a["disk_app_all"])
        worksheet.write(row, 17, a["disk_app_usage"])
        worksheet.write(row, 18, a["disk_sda_rs"])
        worksheet.write(row, 19, a["disk_sda_ws"])
        worksheet.write(row, 20, a["rx_bytes"])
        worksheet.write(row, 21, a["tx_bytes"])
        worksheet.write(row, 22, a["open_port"])
        worksheet.write(row, 23, a["remark"])

        row = row + 1
    # </editor-fold>

    workbook1.close()


if __name__ == '__main__':

    # conf_file = 'E:\\0yunmasfile\\yunmas-jiaoben\\9-moni-dev.txt'  # 本地配置文件
    conf_file = 'E:\\0yunmasfile\\yunmas-jiaoben\\9-moni-pro.txt'  # 本地配置文件
    listall = []

    # 读取本地配置文件
    pd.read_csv(conf_file, sep=' ')
    hostList = pd.read_table(conf_file, encoding='gb2312', delim_whitespace=True, index_col=0)
    print("开始巡检，共计 %s 台主机，请等待....." % len(hostList))
    for index, row in hostList.iterrows():
        print(str(index) + " " + row["ip"])
        # print("ip:" + row["ip"], "uname:" + row["uname"], "pwd:" + row["pwd"], "filename:" + row["filename"])  # 输出各列
        ip = row["ip"]
        username = str(row["uname"])
        password = str(row["pwd"])

        tmplist = {}
        tmplist["id"] = None
        tmplist["ip"] = None  # 1
        tmplist["hostname"] = None  # 2
        tmplist["version"] = None  # 3
        tmplist["current_time"] = None  # 4
        tmplist["operation_time"] = None  # 5
        tmplist["can_login_users"] = None  # 6
        tmplist["can_login_user_num"] = None  # 7
        tmplist["current_users"] = None  # 8
        tmplist["load_average"] = None  # 9
        tmplist["cpu_usage"] = None  # 10
        tmplist["momery_total"] = None  # 11
        tmplist["momery_usage"] = None  # 12
        tmplist["swap_total"] = None  # 13
        tmplist["swap_usage"] = None  # 14
        tmplist["disk_all"] = None  # 15
        tmplist["disk_app_all"] = None  # 16
        tmplist["disk_sda_rs"] = None  # 17
        tmplist["disk_sda_ws"] = None  # 18
        tmplist["disk_app_usage"] = None  # 19
        tmplist["rx_bytes"] = None  # 20
        tmplist["tx_bytes"] = None  # 21
        tmplist["open_port"]=None # 22
        tmplist["remark"] = None  # 23

        s = Server.Server(ip, 22, username, password)  # 实例化
        try:
            s.connect()  # 创建一个连接
            s.open_ssh()  # 开启ssh

            # 2.主机名称
            hostname = s.ssh_send_cmd("hostname")
            # 3.系统版本
            version = s.ssh_send_cmd("cat /etc/redhat-release")
            # 4.系统当前时间
            current_time = s.ssh_send_cmd("uptime | awk  '{print $1}'")
            sleep(1)
            # 5.系统运行时间
            operation_time = s.ssh_send_cmd("uptime | awk  -F '[,]+' '{print $1 $2}'|awk '{$1=\"\";print $0}'")
            # 6.可登陆系统的用户数
            can_login_user_num = s.ssh_send_cmd("cat /etc/passwd | awk -F: '/bash$/{x++} END{print x}'")
            # 7.可登陆系统的用户
            can_login_users = s.ssh_send_cmd("cat /etc/passwd | awk -F: '/bash$/{print $1}' | xargs | sed 's/ /,/g'")
            # 8.当前用户数
            current_users = s.ssh_send_cmd("uptime | awk  -F '[,]+' '{print $3}'")
            sleep(1)
            # 9.负载
            load_average = s.ssh_send_cmd("cat /proc/loadavg")  # uptime | awk -F '[, ]+' '{print $(NF-2),$(NF-1),$NF}'
            sleep(1)

            # 10、CPU使用率
            cpu_usage = s.ssh_send_cmd(
                "top -bn1 |grep Cpu | tail -l| awk -F'id,' '{print $1}'|awk -F'[,]+' '{print (100-$NF)\"%\"}'")

            sleep(1)

            # 内存
            # 11.总的物理内存
            momery_all = s.ssh_send_cmd("free -h | awk '{print $2}' | awk 'NR==2{printf $1}'")
            # 12.物理内容使用率
            ## 对操作系统来说，Buffers和Cached是已经被使用的:MemFree=total-used
            ## 对应用程序来说:MemFree=buffers+cached+free,已使用的：(used – (buffers + cached))/total
            if '6.8' in version:
                momery_usage = s.ssh_send_cmd("free | sed -n '2p' |awk '{printf ($3-($6+$7))/$2*100\"%\"}'")
            elif '7.' in version:
                momery_usage = s.ssh_send_cmd("free | sed -n '2p' |awk '{printf (1-$7/$2)*100\"%\"}'")
            else:
                momery_usage = s.ssh_send_cmd("top -bn1 | awk '/Mem/{print $0}'")
            # 13.Swapd大小:swap used 数值大于 0 ，基本可以判断已经遇到内存瓶颈了，要么优化你的代码，要么加内存。
            swap_total = s.ssh_send_cmd("free -h |awk '/Swap/{printf $2}'")
            # 14.Swap使用率
            swap_usage = s.ssh_send_cmd("free |awk '/Swap/{printf ($3/$2*100)\"%\"}'")

            # ### 磁盘
            # 15.根目录分区大小
            disk_all = s.ssh_send_cmd("df -hP| awk '{print $2}' | awk 'NR==2{print}'")
            # 16./home/yunmas分区大小
            disk_app_all = s.ssh_send_cmd("df -hP /home/yunmas| awk '{print $2}' | awk 'NR==2{print}'")
            # 17./home/yunmas分区使用率
            disk_app_usage = s.ssh_send_cmd("df -hP /home/yunmas/ | sed -n '2p' | awk '{print $5}'")
            sleep(1)

            # 18.每秒向设备发起的读请求次数
            disk_sda_rs = s.ssh_send_cmd("iostat -kx | grep sda| awk '{print $4}'")
            # 19.每秒向设备发起的读请求次数
            disk_sda_ws = s.ssh_send_cmd("iostat -kx | grep sda| awk '{print $5}'")

            # 网络流量
            # 20.接收字节数
            rx_bytes = s.ssh_send_cmd("cat /proc/net/dev | sed -n '4p' | awk '{print $2}'")
            # 21.发送字节数
            tx_bytes = s.ssh_send_cmd("cat /proc/net/dev | sed -n '4p' | awk '{print $10}'")
            sleep(1)
            open_port = s.ssh_send_cmd("netstat -ntpl | awk '{if(NR>2){print $4}}' |awk -F':' '{print $NF}' | awk '!a[$0]++'|sort  -n | xargs | sed 's/ /,/g'")

            tmplist["id"] = index
            tmplist["ip"] = ip  # 1
            tmplist["hostname"] = hostname.replace("\n", "").strip()  # 2
            tmplist["version"] = version.replace("\n", "").strip()  # 3
            tmplist["current_time"] = current_time.replace("\n", "").strip()  # 4
            tmplist["operation_time"] = operation_time.replace("\n", "").strip()  # 5
            tmplist["can_login_user_num"] = can_login_user_num.replace("\n", "").strip()  # 6
            tmplist["can_login_users"] = can_login_users.replace("\n", "").strip()  # 7
            tmplist["current_users"] = current_users.replace("\n", "").strip()  # 8
            tmplist["load_average"] = load_average.replace("\n", "").strip()  # 9
            tmplist["cpu_usage"] = cpu_usage.replace("\n", "").strip()  # 10
            tmplist["momery_total"] = momery_all.replace("\n", "").strip()  # 11
            tmplist["momery_usage"] = momery_usage.replace("\n", "").strip()  # 12
            tmplist["swap_total"] = swap_total.replace("\n", "").strip()  # 13
            tmplist["swap_usage"] = swap_usage.replace("\n", "").strip()  # 14
            tmplist["disk_all"] = disk_all.replace("\n", "").strip()  # 15
            tmplist["disk_app_all"] = disk_app_all.replace("\n", "").strip()  # 16
            tmplist["disk_app_usage"] = disk_app_usage.replace("\n", "").strip()  # 17
            tmplist["disk_sda_rs"] = disk_sda_rs.replace("\n", "").strip()  # 18
            tmplist["disk_sda_ws"] = disk_sda_ws.replace("\n", "").strip()  # 19
            tmplist["rx_bytes"] = rx_bytes.replace("\n", "").strip()  # 20
            tmplist["tx_bytes"] = tx_bytes.replace("\n", "").strip()  # 21
            tmplist["open_port"] = open_port.replace("\n", "").strip()  # 22
            if swap_total.replace("\n", "").strip() > "80%":
                remark = "swap:%s,内存可能不足" % swap_usage
                tmplist["remark"] = remark.replace("\n", "").strip()  # 23
            # print(tmplist)
            listall.append(tmplist)
        except Exception as _e:
            print('异常：%s' % _e)
        finally:
            if s:
                s.close()
                del s

    # print(listall)
    try:
        trywexrestr(listall)
        print("巡检完成，详见导出结果》》》》》》")
    except Exception as _e:
        print('巡检异常：%s' % _e)
