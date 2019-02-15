#! /usr/bin/env bash

if [ $# != 1 ]; then
  echo "Tool to disconnect a wireless interface."
  echo "Usage: $0 <wireless-interface>"
  exit 1
fi

dhclient -r
killall dhclient
ip addr del 192.168.1.2/24 dev $1
ip route del default via 192.168.1.1 dev $1
ip link set $1 down
ip link set $1 up
