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

import time
print(time.time())


def countdown():
    nowtime = datetime.now()
    xbtime = nowtime.replace(hour=17, minute=30, second=0)
    delta = xbtime - nowtime
    print(delta)

    if __name__ == "main":
        while 1 == 1:
            countdown()
            sleep(1)
