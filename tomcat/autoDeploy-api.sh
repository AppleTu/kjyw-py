#! /bin/sh
echo '####################自动部署说明####################'
echo '/home/yunmas下建立如下目录：'
echo '.'
echo '├── autoDeploy.sh          --本脚本存放目录'
echo '├── appBase'
echo '│   └── yunmas_api.war     --新war存放目录'
echo '├── dbbak'
echo '└── tomcat'
echo '    ├── tomcat0'
echo '    ├── tomcat1'
echo '    ├── tomcat2'
echo '    └── tomcat3'

echo '####################开始自动部署####################'
path=`pwd` #当前路径 /home/yunmas

PID=$(ps -ef|grep tomcat|grep -v grep|awk '{print $2}')
echo "tomcatPID:$PID"
if [ -z "$PID" ];
        then
                echo "no tomcat process!"
        else
                ps -ef|grep tomcat|grep -v grep|awk '{print $2}'|xargs kill -9  #./shutdown.sh #停止tomcat服务
                echo "Tomcat process has all been killed."
fi
sleep 1 #休眠1s

#循环部署tomcat
for tomcatPath in /home/yunmas/tomcat/*
do
if [ -d "$tomcatPath" ]
then
        echo "$tomcatPath is directory"
        #进入tomcat的webapps目录
        cd $tomcatPath/webapps
        #删除旧项目文件目录：yunmas_api
        rm -fr yunmas_api
        #备份webapps下的旧war包：yunmas_api.war
        mv yunmas_api.war $path/dbbak/yunmas_api.war.$(date +%Y%m%d%H%M%S%N)
        #复制新的war包：yunmas_api.war 到webapps路径下
        cp $path/appBase/yunmas_api.war yunmas_api.war
        #休眠1s
        sleep 1
        cd ../bin
        ./startup.sh #启动tomcat服务
        #tail -f $tomcatPath/logs/catalina.out
        #休眠1s
        sleep 1
        echo '####################':${tomcatPath##*/}'部署成功####################'
elif [ -f "$tomcatPath" ]
then
        echo "$tomcatPath is file"
fi
done

echo '#####################tomcat实例部署结束####################'
