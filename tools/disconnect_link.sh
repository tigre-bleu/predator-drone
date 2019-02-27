#! /usr/bin/env bash
#
# Disconnect from WLAN
#


# Check root privileges
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root!"
  exit
fi


# Check arguments
if [ "$#" -ne 1 ] || [ ! -d "/sys/class/net/$1" ]; then
  echo "Tool to disconnect a wireless interface"
  echo ""
  echo "Usage: $0 <wireless-interface>"
  echo "  with <wireless-interface> in:"
  ls /sys/class/net
  exit
fi


# Disconnect
dhclient -r
iw $1 disconnect
ip link set $1 down
ip link set $1 up

