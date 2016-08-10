# Kubernetes The Hard Way - Look Ma NoCloud Version !

This tutorial is based the excellent tutorial by kelseyhightower. I have edited it to use NoCloud aka only local KVM VMs and some more modified components. It's by no means as robust, but gives you more control over all the moving parts. 

Network setup - we are going to simplify the networking configuration by using dnsmaq

Create a linux bridge - lxcbr0 and attach it to an outgoing interface so that all the machines have access to the Internet. 

dnsmasq --conf-file=/etc/lxc/dnsmasq.conf -u lxc-dnsmasq --strict-order --bind-interfaces --pid-file=/run/lxc/dnsmasq.pid --listen-address 10.0.3.1 --dhcp-range 10.0.3.2,10.0.3.254 --dhcp-lease-max=253 --dhcp-no-override --except-interface=lo --interface=lxcbr0 --dhcp-leasefile=/var/lib/misc/dnsmasq.lxcbr0.leases --dhcp-authoritative

Edit these 3 files - (I have piggybacked on the existing installation of lxc, plan to redo this with a cleaner config soon.)


/etc/dnsmasq.d/lxc - Contains the following for reverse DNS resolution

# Tell any system-wide dnsmasq instance to make sure to bind to interfaces
# instead of listening on 0.0.0.0
# WARNING: changes to this file will get lost if lxc is removed.
bind-interfaces
except-interface=lxcbr0

ptr-address=20.3.0.10.in-addr,arpa,node0.24.io
ptr-address=21.3.0.10.in-addr,arpa,node1.24.io
ptr-address=22.3.0.10.in-addr,arpa,node2.24.io
ptr-address=23.3.0.10.in-addr,arpa,node3.24.io
ptr-address=24.3.0.10.in-addr,arpa,node4.24.io
ptr-address=25.3.0.10.in-addr,arpa,node5.24.io
ptr-address=26.3.0.10.in-addr,arpa,node6.24.io
ptr-address=27.3.0.10.in-addr,arpa,node7.24.io
ptr-address=28.3.0.10.in-addr,arpa,node8.24.io
ptr-address=29.3.0.10.in-addr,arpa,node9.24.io
ptr-address=19.3.0.10.in-addr,arpa,controller.24.io
ptr-address=30.3.0.10.in-addr,arpa,lbfe.24.io
ptr-address=31.3.0.10.in-addr,arpa,lbbe1.24.io
ptr-address=32.3.0.10.in-addr,arpa,lbbe2.24.io
ptr-address=33.3.0.10.in-addr,arpa,lbbe3.24.io


/etc/lxc/dnsmasq.conf - Contains the following for DHCP address reservation

dhcp-host=node0,10.0.3.20
dhcp-host=node1,10.0.3.21
dhcp-host=node2,10.0.3.22
dhcp-host=node3,10.0.3.23
dhcp-host=node4,10.0.3.24
dhcp-host=node5,10.0.3.25
dhcp-host=node6,10.0.3.26
dhcp-host=node7,10.0.3.27
dhcp-host=node8,10.0.3.28
dhcp-host=node9,10.0.3.29
dhcp-host=controller,10.0.3.19
dhcp-host=lbfe,10.0.3.30
dhcp-host=lbbe1,10.0.3.31
dhcp-host=lbbe2,10.0.3.32
dhcp-host=lbbe3,10.0.3.33

/etc/hosts - Contains the following for DNS resolution


10.0.3.20 node0 node0.24.io
10.0.3.21 node1 node1.24.io
10.0.3.22 node2 node2.24.io
10.0.3.23 node3 node3.24.io
10.0.3.24 node4 node4.24.io
10.0.3.25 node5 node5.24.io
10.0.3.26 node6 node6.24.io
10.0.3.27 node7 node7.24.io
10.0.3.28 node8 node8.24.io
10.0.3.29 node9 node9.24.io
10.0.3.19 controller controller.24.io

10.0.3.30 lbfe lbfe.24.io
10.0.3.31 lbbe1 lbbe1.24.io
10.0.3.32 lbbe2 lbbe2.24.io
10.0.3.33 lbbe3 lbbe3.24.io


