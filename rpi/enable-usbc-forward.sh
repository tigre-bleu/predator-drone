#! /bin/sh
#
# Enable NAT for RpiW0
#
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A POSTROUTING -o enp60s0u1u4 -j MASQUERADE
