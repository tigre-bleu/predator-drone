#! /bin/sh
#
# Enable NAT for RpiW0
#
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A POSTROUTING -o enp0s20f0u2 -j MASQUERADE
