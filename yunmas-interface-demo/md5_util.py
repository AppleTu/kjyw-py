# -*- coding: utf-8 -*-
# @Time    : 2020/8/6 10:05
# @Author  : lp
# @desc    : 老板你再这样我要删库了

# hexdigest实际上返回的是16进制的str形式，digest返回的是bytes
import base64
import hashlib


def md5(text):
    """md5加密函数"""
    md5 = hashlib.md5()
    if not isinstance(text, bytes):
        text = str(text).encode('utf-8')
    md5.update(text)
    return md5.hexdigest()


def md5_digest(text):
    """md5加密函数"""
    md5 = hashlib.md5()
    if not isinstance(text, bytes):
        text = str(text).encode('utf-8')
    md5.update(text)
    return md5.digest()

def base64_encode_digest(text):
    """进行base64编码处理"""
    return base64.b64encode(text)

if __name__ == '__main__':
    print('qzKAvAJEJUH3Gz9uqYl8LleqKxYPRgg2aTCwVKKMQNcjZp6GeR20200806100648wVKKMQNcjZp6GeR')
    print(md5('qzKAvAJEJUH3Gz9uqYl8LleqKxYPRgg2aTCwVKKMQNcjZp6GeR20200806100648wVKKMQNcjZp6GeR'))
    print(base64_encode_digest(md5_digest('qzKAvAJEJUH3Gz9uqYl8LleqKxYPRgg2aTCwVKKMQNcjZp6GeR20200806100648wVKKMQNcjZp6GeR')))