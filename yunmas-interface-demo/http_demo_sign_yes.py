
import datetime
import hashlib
import json

import requests

# hexdigest实际上返回的是16进制的str形式，digest返回的是bytes
def md5(text):
    """md5加密函数"""
    md5 = hashlib.md5()
    if not isinstance(text, bytes):
        text = str(text).encode('utf-8')
    md5.update(text)
    return md5.hexdigest()

url = 'http://api.eyun.openmas.net:8080/yunmas_api/smsApi/batchSendMessage'
headers = {
    "Content-Type": "application/json; charset=utf-8"
}
_applicationId = ''
_password = ''
_request_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 获取系统当前时间
_sign = ''
_sign_plaintext = _applicationId + _password + _request_time + _sign
_sign_ciphertext = md5(_sign_plaintext)  # 令牌生成规则：MD5Util.MD5(applicationId+password+requestTime+sign令牌)
# _sign_ciphertext='4cda9db338850a1f895fecdad83873f5'
print(_sign_ciphertext)
postdatas = {
    "applicationId": _applicationId,
    "password": _password,
    "requestTime": _request_time,
    "sign": _sign_ciphertext,
    "funCode": "1002",
    "extendCode": "8888",  # 自定义扩展号: 必须为数字，且 接入号+扩展号 总长度不能超过20位
    "mobiles": ["18767126025","18767126025","18767126025"],
    "content": "这是一条 Python 提交的测试短信(sign版)。"
}
# print(postdatas)
print(json.dumps(postdatas, ensure_ascii=False, indent=4))  # json格式化打印,ensure_ascii=False 转中文

response = requests.post(url=url, headers=headers, json=postdatas)
request = response.text.encode('utf-8').decode('unicode_escape')    #对请求结果进行编码转换，转换成汉字
print(response.text)      # 不转换返回的结果
# print(request)          # 转换返回的结果



