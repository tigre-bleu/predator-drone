#! /usr/bin/env bash
#
# Install predator-drone requirements and configure Raspberry Pi Zero W:
#   - WiFi hotspot on wlan0 (integrated wireless card)   => 172.20.1.1
#   - Bluetooth PAN on pan0 (bluetooth bridge interface) => 172.20.2.1
#


# Check root privileges
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root!"
  exit
fi


# =========================
#    Access point config
# =========================

# Install requirements
apt install hostapd dnsmasq
systemctl stop hostapd
systemctl stop dnsmasq


# Configure static IP
cat >>/etc/dhcpcd.conf <<EOF

# Configure static IP on WiFi hotspot
interface wlan0
static ip_address=172.20.1.1/24
EOF


# Configure DHCP server
mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
cat >/etc/dnsmasq.conf <<EOF
interface=wlan0
  listen-address=172.20.1.1
  dhcp-range=172.20.1.10,172.20.1.30,255.255.255.0,24h
EOF


# Configure hotspot
cat >/etc/hostapd/hostapd.conf <<EOF
# Create hotspot on wlan0 interface
interface=wlan0

# WiFi mode: IEEE 802.11b, on channel 10
hw_mode=b
channel=10

# Visible SSID
ssid=Predator-drone-controller
ignore_broadcast_ssid=0

# Authentication: WPA-PSK (TKIP/CCMP)
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP

wpa_passphrase=pdc12345
EOF

sed "s:^DAEMON_CONF=.*$:DAEMON_CONF=/etc/hostapd/hostapd.conf:" /etc/init.d/hostapd > /tmp/hostapd
cat /tmp/hostapd >/etc/hostapd/hostapd.conf
rm  /tmp/hostapd


# Enable services
systemctl enable hostapd
systemctl enable dnsmasq


# Start services
systemctl start hostapd
systemctl start dnsmasq



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
Address=172.20.2.1/24
DHCPServer=no
EOF


# Configure static IP
cat >>/etc/dhcpcd.conf <<EOF

# Configure static IP on Bluetooth PAN
interface pan0
static ip_address=172.20.2.1/24
EOF


# Configure DHCP server
mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
cat >>/etc/dnsmasq.conf <<EOF

interface=pan0
  listen-address=172.20.2.1
  dhcp-range=172.20.2.10,172.20.2.30,255.255.255.0,24h
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


# Enable services
systemctl daemon-reload
systemctl enable systemd-networkd
systemctl enable bt-agent
systemctl enable bt-network


# Start services
systemctl start systemd-networkd
systemctl start bt-agent
systemctl start bt-network
systemctl restart dnsmasq


# Pair device
bt-adapter --set Discoverable 1
echo "Pair your device with the Raspberry Pi then hit CTRL-C..."
read -r -d '' _
bt-adapter --set Discoverable 0



# ==========================
#    Exploit requirements
# ==========================

apt install npm python3
pip3 install pyric

