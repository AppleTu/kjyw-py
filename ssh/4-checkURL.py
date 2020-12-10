# -*- coding: utf-8 -*-
# @Time    : 2020/4/14 17:05
# @Author  : lp
# @desc    : 老板你再这样我要删库了

# 验证是否部署成功
import time
import requests
import urllib3

# urllist=['http://eyun.openmas.net/login/',
#          'http://man.eyun.openmas.net/login',
#          'http://eyun.openmas.net/',
#          'http://man.eyun.openmas.net/',
#          'http://api.eyun.openmas.net/yunmas_api/ws/wsApi?wsdl',
#          'http://api.eyun.openmas.net/yunmas_api/smsApi/batchSendMessage',
#          'http://api.eyun.openmas.net/yunmas_api/SendMessageServlet']
urllist=['http://188.102.17.194:8080/login/', # 企业门户
         'http://188.102.17.195:8080/login/', # 企业门户
         'http://188.102.17.196:8080/login/', # 企业门户
         'http://188.102.17.196:8080/login/', # 管理门户

         'http://188.102.17.198:8080/yunmas_api/ws/wsApi?wsdl', # API
         'http://188.102.17.198:8081/yunmas_api/ws/wsApi?wsdl', # API
         'http://188.102.17.198:8082/yunmas_api/ws/wsApi?wsdl', # API
         'http://188.102.17.198:8083/yunmas_api/ws/wsApi?wsdl', # API

         'http://188.102.17.198:8080/yunmas_api/smsApi/batchSendMessage', # API
         'http://188.102.17.198:8081/yunmas_api/smsApi/batchSendMessage', # API
         'http://188.102.17.198:8082/yunmas_api/smsApi/batchSendMessage', # API
         'http://188.102.17.198:8083/yunmas_api/smsApi/batchSendMessage', # API

         'http://188.102.17.198:8080/yunmas_api/SendMessageServlet', # API
         'http://188.102.17.198:8081/yunmas_api/SendMessageServlet', # API
         'http://188.102.17.198:8082/yunmas_api/SendMessageServlet', # API
         'http://188.102.17.198:8083/yunmas_api/SendMessageServlet', # API

         'http://188.102.17.199:8080/yunmas_api/ws/wsApi?wsdl', # API
         'http://188.102.17.199:8080/yunmas_api/smsApi/batchSendMessage', # API
         'http://188.102.17.199:8080/yunmas_api/SendMessageServlet', # API

         'http://188.102.17.200:8080/yunmas_api/ws/wsApi?wsdl', # API
         'http://188.102.17.200:8081/yunmas_api/ws/wsApi?wsdl', # API
         'http://188.102.17.200:8082/yunmas_api/ws/wsApi?wsdl', # API
         'http://188.102.17.200:8083/yunmas_api/ws/wsApi?wsdl', # API

         'http://188.102.17.200:8080/yunmas_api/smsApi/batchSendMessage', # API
         'http://188.102.17.200:8081/yunmas_api/smsApi/batchSendMessage', # API
         'http://188.102.17.200:8082/yunmas_api/smsApi/batchSendMessage', # API
         'http://188.102.17.200:8083/yunmas_api/smsApi/batchSendMessage', # API

         'http://188.102.17.200:8080/yunmas_api/SendMessageServlet', # API
         'http://188.102.17.200:8081/yunmas_api/SendMessageServlet', # API
         'http://188.102.17.200:8082/yunmas_api/SendMessageServlet', # API
         'http://188.102.17.200:8083/yunmas_api/SendMessageServlet', # API

         ]
print('开始检查URL：')
header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3298.4 Safari/537.36'
    }
for url in urllist:
    # print('❤ request check url is == ' + url)
    urllib3.disable_warnings()
    try:
        # req = urllib.request.Request(url)
        # req.add_header('User-Agent',
        #                'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')
        # resp =urllib.request.urlopen(url, timeout=1)
        resp = requests.get(
            url, headers=header, verify=False, allow_redirects=False
        )
        code = resp.status_code
        print(code,'❤ request check url==' + url)
    except Exception  as e:
        print(url,":",e)
        time.sleep(2)

def disable_warnings():
    """
    解除去掉证书后总是抛出异常告警
    """
    urllib3.disable_warnings()