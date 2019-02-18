#! /bin/sh
#
# Enable NAT for RpiW0
#


# Check root privileges
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root!"
  exit
fi


# Check arguments
if [ "$#" -ne 1 ] || [ ! -d "/sys/class/net/$1" ]; then
  echo "Share internet with Raspberry Pi"
  echo ""
  echo "Usage: $0 <output-interface>"
  echo "  with <output-interface> in:"
  ls /sys/class/net
  exit
fi

# Enable routing
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A POSTROUTING -o $1 -j MASQUERADE

