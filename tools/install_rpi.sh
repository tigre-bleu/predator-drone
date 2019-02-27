#! /usr/bin/env bash
#
# Install predator-drone requirements and configure Raspberry Pi Zero W:
#   - Bluetooth PAN on pan0 (bluetooth bridge interface)
#      + IPv4: 172.20.1.1
#      + IPv4: 172.20.1.10 (listening for Parrot control thanks to NAT)
#      + no DHCP server
#


# Check root privileges
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root!"
  exit
fi



# ==========================
#    Bluetooth PAN config
# ==========================

# Steps taken from: https://raspberrypi.stackexchange.com/a/71587

# Install requirements
apt install bluez bluez-tools


# Configure a new network adapter
cat >/etc/systemd/network/pan0.netdev <<EOF
[NetDev]
Name=pan0
Kind=bridge
EOF

cat >/etc/systemd/network/pan0.network <<EOF
[Match]
Name=pan0

[Network]
Address=172.20.1.1/24
DHCPServer=no
EOF


# Configure Bluetooth agent
cat >/etc/systemd/system/bt-agent.service <<EOF
[Unit]
Description=Bluetooth Auth Agent

[Service]
ExecStart=/usr/bin/bt-agent -c NoInputNoOutput
Type=simple

[Install]
WantedBy=multi-user.target
EOF

cat >/etc/systemd/system/bt-network.service <<EOF
[Unit]
Description=Bluetooth NEP PAN
After=pan0.network

[Service]
ExecStart=/usr/bin/bt-network -s nap pan0
Type=simple

[Install]
WantedBy=multi-user.target
EOF


# Configure static IP and disable wpa_supplicant
cat >>/etc/dhcpcd.conf <<EOF

# Configure static IP on Bluetooth PAN
interface pan0
  static ip_address=172.20.2.1/24
  static ip_address=172.20.2.10/24
  nohook wpa_supplicant

# Don't run wpa_supplicant
interface wlan0
  nohook wpa_supplicant
interface wlan1
  nohook wpa_supplicant

# Disable DHCP requests on wlan
denyinterfaces wlan0 wlan1
EOF


# Enable and start services
systemctl daemon-reload

systemctl enable systemd-networkd
systemctl enable dhcpcd
systemctl enable bt-agent
systemctl enable bt-network

systemctl restart systemd-networkd
systemctl restart dhcpcd
systemctl start bt-agent
systemctl start bt-network


# Enable IP forwarding
sysctl -w net.ipv4.ip_forward=1
sed "s:^#net.ipv4.ip_forward=1:net.ipv4.ip_forward=1:" /etc/init.d/hostapd > /tmp/sysctl.conf
cat /tmp/sysctl.conf >/etc/sysctl.conf
rm  /tmp/sysctl.conf



# =======================
#    Bluetooth pairing
# =======================

bt-adapter --set Discoverable 1
echo "Pair your device with the Raspberry Pi then hit CTRL-C..."
read -r -d '' _
bt-adapter --set Discoverable 0



# ==========================
#    Exploit requirements
# ==========================

apt install python3 aircrack-ng dhclient iptables python3-pip
pip3 install pyric scapy

