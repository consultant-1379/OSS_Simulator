#!/bin/bash

HOST=`hostname`
IP=`grep "$HOST" /etc/hosts | cut -d" " -f1`

setup_rsh()
{


grep "netsim" /etc/hosts
if [ $? -ne 0 ];then
	cat /etc/hosts > /tmp/hosts_tmp
	echo "$IP netsim"  >> /tmp/hosts_tmp
	mv /tmp/hosts_tmp /etc/hosts
fi

cat /etc/pam.d/rsh | grep "#session" | grep "pam_keyinit.so"
if [ $? -ne 0 ];then
	sed -i '/pam_keyinit\.so/s/^/#/' /etc/pam.d/rsh
fi

cat /etc/pam.d/rsh | grep "#session" | grep "pam_loginuid.so"
if [ $? -ne 0 ];then
	sed -i '/pam_loginuid\.so/s/^/#/' /etc/pam.d/rsh
fi

echo "+ +" > /etc/hosts.equiv

grep "rsh" /etc/securetty
if [ $? -ne 0 ];then
	echo "rsh" >> /etc/securetty
fi

grep "netsim" ~/.rhosts 2> /dev/null
if [ $? -ne 0 ];then
	echo "$IP netsim"  >> ~/.rhosts
fi
}

unmount_dirs()
{

mount | grep pms_tmpfs | cut -d" " -f3 > /tmp/mounted_dirs
while read line
do
	unount $line
done </tmp/mounted_dirs


}
setup_rsh
unmount_dirs
