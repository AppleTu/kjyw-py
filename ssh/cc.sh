#!/bin/bash

echo -e "Hostname :" $tecreset $HOSTNAME


internalip=$(hostname -I)
echo -e "Internal IP :" $tecreset $internalip


cpuusage=$(sar -u 1 5 | awk '{print (100-$9)}' | sed -n '7p')
echo "CPU Usage:"${cpuusage}%

disk_percent=$(df -lh | grep -w '\/' | awk '{print $(NF-1)}')
echo "Disk_percent:"${disk_percent}%


memery_used_k=$(free | grep 'Mem' | awk '{print $3}')
memery_all_k=$(free | grep 'Mem' | awk '{print $2}')
memery_percent=`echo ${memery_used_k} ${memery_all_k} | awk '{printf "%.2f", $1/$2*100}'`
echo "Memery_percent:"${memery_percent}%


