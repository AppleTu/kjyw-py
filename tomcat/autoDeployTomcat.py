# -*- coding: utf-8 -*-
# @Time    : 2020/3/23 9:45
# @Author  : lp
# @desc    : 多实例tomcat自动安装：这里是指在单机上安装多个tomcat实例
'''
应用场景：在生产环境，单机安装多个实例。
传统简单方式：复制多份tomcat安装文件。缺点：占空间，升级麻烦，当存在多个实例时，升级时又得重新复制多份，也容易导致多个实例的tomcat版本不一致。
现在想法是：tomcat核心文件只一份，复制多份配置文件，即实现多实例
'''
import os
import shutil

'''
tomcat各目录的作用：
bin：存放脚本文件，例如启停脚本 startup.sh shutdown.sh
conf：存放配置文件，最主要的是server.xml 和 web.xml
lib：存放各种依赖jar包
logs：存放日志文件
temp：存放tomcat运行时产生的临时文件
webapps：应用部署目录
work：主要存放由JSP文件生成的servlet（java文件以及最终编译生成的class文件）

部署过程：
1.官方源码包路径：/home/yunmas/yunmas-tomcat-src
2.创建实例目录 yunmas-tomcat，然后每个实例主目录以tomcat0，tomcat1，tomcat2...命名，结构如下：
yunmas-tomcat
   ├── tomcat0
   ├── tomcat1
   ├── tomcat...
   └── tomcatN
3.修改server.xml配置文件：
主要修改监听端口、关闭端口、应用部署目录，修改方式，源文件
监控端口：默认是8080，定义为$port，因为是多实例，所以各个实例的端口都不能一样，并且不能被其它程序占用，这里选用8080+n的方式生成，n为tomcat实例个数 
关闭端口：默认是8005，定义为$shutdownPort，这里选用8010+n的方式生成，n为tomcat实例个数 
应用部署目录：appbase参数，默认是webapps，定义为$appbase
配置web应用目录：docBase参数，默认是webapps，定义为$docBase,无web界面的可不配置
4.
'''

class DeployTomcat():
    BASE_DIR = "/home/yunmas"  ##the base dir of installed software
    # BASE_DIR = "D:\\project\\PycharmProjects\\pyAutoDeplo"  ##the base dir of installed software
    APP_DIR = BASE_DIR + os.sep + "appBase"

    TOMCAT_DIR_SRC = BASE_DIR + os.sep + "yunmas-tomcat-src"
    TOMCAT_DIR_HOME=BASE_DIR + os.sep + "tomcat"

    # 创建实例目录
    def deployTomcat(self,num,appBase,docBase):
        for i in range(num):
            # *定义一个变量判断tomcat实例目录是否存在*
            isExists = os.path.exists(self.TOMCAT_DIR_HOME + os.sep + 'tomcat' + str(i))
            if not isExists:
                tomInstance_dir = self.TOMCAT_DIR_HOME + os.sep + 'tomcat'+str(i)

                # os.makedirs(tomInstance_dir) 创建实例路径
                # 拷贝一个tomcat实例到/home/yunmas/tomcat/tomcat0...
                shutil.copytree(self.TOMCAT_DIR_SRC, tomInstance_dir)

                #配置server.xml
                tomcat_server_conf = tomInstance_dir+ os.sep +'conf'+ os.sep +'server.xml'
                shutdownPort=8010+i
                port=8080+i
                #self.confServerXml(self,tomcat_server_conf,shutdownPort,port,appBase,docBase)
                with open(tomcat_server_conf) as source:
                    contens = source.read()
                    contens = contens.replace("$shutdownPort", str(shutdownPort)).replace("$port", str(port)).replace(
                        "$appBase", str(appBase)).replace("$docBase",str(docBase))
                    with open(tomcat_server_conf, "w") as des:
                        des.write(contens)

                print("✔ tomcat%s 实例创建并配置成功" % i)  # √
            else:
                print("✘ tomcat%s 实例已经存在,请先删除" % i) # ×
                continue  # 如果文件不存在,则继续上述操作,直到循环结束


if __name__ == '__main__':
    # 声明字符串数组并初始化
    appList = ['1.yunmas_biz', '2.yunmas_man', '3.yunmas_api', '4.yunmas_sms', '5.yunmas_redis']
    # 字符串数组的输出
    for i in range(len(appList)):
        print('%s  ' % appList[i])

    try:
        choice = int(input('请输入选择:'))
        # 输入的判断
        if choice == 1:
            print('开始部署 %s ...' % appList[choice - 1])
            DeployTomcat().deployTomcat(1, 'webapps', 'yunmas_biz')
        elif choice == 2:
            print('开始部署 %s ...' % appList[choice - 2])
            DeployTomcat().deployTomcat(1, 'webapps', 'yunmas_man')
        elif choice == 3:
            print('开始部署 %s ...' % appList[choice - 3])
            DeployTomcat().deployTomcat(4, 'webapps', 'yunmas_api')
        elif choice == 4:
            print('开始部署 %s ...' % appList[choice - 4])
            DeployTomcat().deployTomcat(10, 'webapps', 'yunmas_sms')
        elif choice == 5:
            print('开始部署 %s ...' % appList[choice - 5])
            DeployTomcat().deployTomcat(3, 'webapps', 'yunmas_redis')
        else:
            print('选择错误，请输入选项的数字！')
    except ValueError:
        print('输入的不是数字，请输入选项的数字！')

