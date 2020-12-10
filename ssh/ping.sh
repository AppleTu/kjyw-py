#!/bin/bash
for ip in $(cat /home/yunmas/moni/ip-list|sed "/^#/d")
do
  ping -c 1 $ip &>/dev/null 
  a=$?
  sleep 2
  ping -c 1 $ip &>/dev/null
  b=$?
  sleep 2
  ping -c 1 $ip &>/dev/null
  c=$?
  sleep 2
  DATE=$(date +%F" "%H:%M)
  if [ $a -ne 0 -a $b -ne 0 -a $c -ne 0 ];then
    #echo "$DATE : $ip Ping is failed." >> /home/yunmas/moni/pinglog.log
    echo "$DATE : $ip Ping is failed."  2>&1 | tee -a /home/yunmas/moni/pinglog.log
  #else
    #echo "$DATE : $ip ping is successful.">> /home/yunmas/moni/pinglog.log
    #echo "$DATE : $ip ping is successful." 2>&1 | tee -a /home/yunmas/moni/pinglog.log
  fi
done
echo "ping ok."