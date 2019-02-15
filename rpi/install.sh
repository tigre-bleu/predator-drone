sudo apt update
sudo apt upgrade
sudo apt install -y hostapd dnsmasq
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq

# Configure static IP
sudo vim /etc/dhcpcd.conf

# Configure DHCP server
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo vim /etc/dnsmasq.conf

# Configure hotspot
sudo vim /etc/hostapd/hostapd.conf
sudo vim /etc/init.d/hostapd
# => change DAEMON_CONF location

sudo apt install aircrack-ng
sudo apt install npm
#include nodejs

# Configure Bluetooth PAN
# https://raspberrypi.stackexchange.com/a/71587
apt install bluez bluez-tools

