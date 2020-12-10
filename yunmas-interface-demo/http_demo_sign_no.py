# -*- coding: utf-8 -*-
# @Time    : 2020/8/6 8:24
# @Author  : lp
# @desc    : 老板你再这样我要删库了


import requests

url = 'http://api.eyun.openmas.net/yunmas_api/smsApi/batchSendMessage'
headers = {
    "Content-Type": "application/json; charset=utf-8"
}
postdatas = {
    "applicationId": "BwlZMcqlf9Crwceqdt6ztEsLzZY8ImQ94oL",
    "password": "RlQWCi1nk9a4vF3",
    "requestTime": "20200805175950",
    # "sign": "01c13a4a9d98dc58f2b469cee35357e3",
    "funCode": "1002",
    "extendCode": "8888",  # 自定义扩展号: 必须为数字，且 接入号+扩展号 总长度不能超过20位
    "mobiles": ["13700000001"],
    "content": "你好,这是一条测试短信。"
}

response = requests.post(url=url, headers=headers, json=postdatas)
request = response.text.encode('utf-8').decode('unicode_escape')    #对请求结果进行编码转换，转换成汉字
print(response.text)    # 不转换返回的结果
#print(request)          # 转换返回的结果
