#!/bin/sh

for vm in "gateway lbfe controller node0 node1 node2 node3 node4 node5 node6 node7 node8 node9"
do 

	echo "Creating - $vm"

	export NODE=controller

	sed "s/node0/$NODE/g" template/cloud-init-user-data > cloud-init-user-data-$NODE

	cloud-localds  cloud-init-user-data-seed-$NODE.img cloud-init-user-data-$NODE

	qemu-img convert yakkety-server-cloudimg-amd64.orig.img yakkety-server-cloudimg-amd64-$NODE.raw

	qemu-img resize -f raw yakkety-server-cloudimg-amd64-$NODE.raw +15G

	#rm -rfv yakkety-64-c-init-$NODE.xml

	sed "s/cloud-init-user-data-seed-node0.img/cloud-init-user-data-seed-$NODE.img/g" template/yakketty-64-c-init.xml > yakkety-64-c-init-$NODE.xml

	sed -i "s/yakkety-server-cloudimg-amd64-node0.raw/yakkety-server-cloudimg-amd64-$NODE.raw/g" yakkety-64-c-init-$NODE.xml

	export UUIDGEN=`uuidgen`

	#UUID c012368b-d7bc-4360-9a0e-733da8158336

	sed -i "s/c012368b-d7bc-4360-9a0e-733da8158336/$UUIDGEN/g" yakkety-64-c-init-$NODE.xml 

	#MAC 52:54:00:ef:be:8c

	MACGEN=$(printf '52:54:00:%02X:%02X:%02X\n' $[RANDOM%256] $[RANDOM%256] $[RANDOM%256])

	#printf '00:60:2F:%02X:%02X:%02X\n' $[RANDOM%256] $[RANDOM%256] $[RANDOM%256]

	sed -i "s/52:54:00:ef:be:8c/$MACGEN/g" yakkety-64-c-init-$NODE.xml 

	#Change the domain name 

	sed -i "s/yaketty-64-c-init/yaketty-64-c-init-$NODE/g" yakkety-64-c-init-$NODE.xml 

	virsh create yakkety-64-c-init-$NODE.xml

	unset MACGEN
	unset UUIDGEN
	unset NODE


done 

