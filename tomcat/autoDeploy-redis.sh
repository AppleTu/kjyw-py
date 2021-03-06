#! /bin/sh
echo '####################自动部署说明####################'
echo '/home/yunmas下建立如下目录：'
echo '.'
echo '├── autoDeploy.sh          --本脚本存放目录'
echo '├── appBase'
echo '│   └── yunmas_redis.war   --新war存放目录'
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
        #删除旧项目文件目录：yunmas_redis
        rm -fr yunmas_redis
        #备份webapps下的旧war包：yunmas_redis.war
        mv yunmas_redis.war $path/dbbak/yunmas_redis.war.$(date +%Y%m%d%H%M%S%N)
        #复制新的war包：yunmas_redis.war 到webapps路径下
        cp $path/appBase/yunmas_redis.war yunmas_redis.war
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
