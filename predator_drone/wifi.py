#
# Wifi management tool
#

from scapy.all import Dot11, Dot11FCS, IP, Dot11Beacon, sniff
from scapy.all import RadioTap, Dot11Deauth, sendp

import pyric.pyw as pyw
import pyric
import time

from .ext_exec import do
from . import disp



# ============================================
#    Access point and client representation
# ============================================

class AccessPoint:
    def __init__(self, ssid, bssid, channel, crypto):
        self.ssid   = ssid
        self.bssid  = bssid
        self.chan   = channel
        self.crypto = crypto
        self.ipv4   = None

    def __str__(self):
        return "AP " + self.bssid                           \
            + " with SSID " + self.ssid                     \
            + " on channel " + str(self.chan)               \
            + " (" + ' / '.join(self.crypto)                \
            + ", IPv4=" + (self.ipv4 or "unknown") + ")"

    def short_str(self):
        return self.ssid + " (" + self.bssid                \
                + ", IPv4=" + (self.ipv4 or "unknown") + ")"

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

MODE_MON = "monitor"
MODE_MAN = "managed"

class WifiManager:
    WIFI_CHAN_MIN = 1
    WIFI_CHAN_MAX = 13


    def __init__(self, iface, mon_mode=False):
        self.detected_aps = []
        self.iface_no_mon = iface.replace("mon", "")

        # Check interface is wireless
        self.card = None
        if not pyw.iswireless(iface):
            disp.die(iface, "is not a wireless interface!\n",
                    "   Available interfaces: ", pyw.winterfaces())

        # Register card
        self.card = pyw.getcard(iface)

        # Set mode according to request
        self.__set_mode(MODE_MON if mon_mode else MODE_MAN)


    def __del__(self):
        # Go to managed mode
        #if self.card != None:
        #    self.__set_mode(MODE_MAN)
        pass



    # =======================
    #    Device management
    # =======================

    def __set_channel(self, channel):
        disp.debug("Changing channel to", str(channel), "for card", self.card.dev)
        pyw.chset(self.card, channel)


    def __get_mode(self):
        return pyw.devinfo(self.card)['mode']

    def __check_mode(self, mode):
        if not self.__get_mode() == mode:
            disp.die(iface_name, "isn't in", mode, "mode!")

    def __set_mode(self, mode):
        disp.debug("Switching adapter to", mode, "mode")

        # Check for supported mode
        if mode not in pyw.devmodes(self.card):
            disp.die(iface_name, "does not support monitor mode!")

        # Check for already enabled mode
        elif self.__get_mode() == mode:
            disp.warn("Wireless card already in", mode, "mode!")

        # Change mode
        else:
            iface = self.iface_no_mon + ("mon" if mode == MODE_MON else "")
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
        self.__check_mode(MODE_MON)

        disp.info("Searching for new running APs")
        for chan in range(self.WIFI_CHAN_MIN, self.WIFI_CHAN_MAX + 1):
            self.__set_channel(chan)
            sniff(iface=self.card.dev, timeout=0.1, lfilter=self.__f_beacon_probe_resp,
                    prn=self.__add_access_point)


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
        """ Filter wifi packets of a specific BSSID, addressed to/from AP. """
        return ( p.haslayer(Dot11) or p.haslayer(Dot11FCS) )   \
                and p.addr3 == bssid and p.haslayer(IP)        \
                and (p.addr1 == p.addr3 or p.addr2 == p.addr3)


    def __add_ssid_client(self, reg_client, p):
        """ Register client of a specific BSSID. """
        # Extract informations
        mac_dst = p.addr1
        mac_src = p.addr2
        bssid   = p.addr3

        ip_dst = p[IP].dst
        ip_src = p[IP].src

        mac   = mac_src   if mac_src != bssid     else mac_dst
        ip    = ip_src    if mac_src != bssid     else ip_dst
        ap_ip = ip_src    if mac_src == bssid     else ip_dst

        # Register client
        reg_client(Client(mac, ip), ap_ip)


    def search_clients(self, ap, reg_client):
        """
        Search for new clients.
        
        : param ap          The access point for which search clients
        : param reg_client  A callback called when a client is found
        """
        self.__check_mode(MODE_MON)
        self.__set_channel(ap.chan)
        sniff(iface=self.card.dev,
                lfilter=lambda p: self.__f_bssid_clients(ap.bssid,   p),
                prn    =lambda p: self.__add_ssid_client(reg_client, p),
                timeout=1)



    # =======================
    #    Client management
    # =======================

    def deauth_client(self, client, ap, dont_stop=False):
        self.__check_mode(MODE_MON)
        self.__set_channel(ap.chan)

        # Send deauth with aireplay
        do("aireplay-ng",
                "-0", '0' if dont_stop else '3',
                "-a", ap.bssid,
                "-c", client.mac,
                self.card.dev)


    def connect_access_point(self, ap, force=True):
        self.__check_mode(MODE_MAN)
        pyw.connect(self.card, ap.ssid.encode(), bssid=ap.bssid)
        time.sleep(0.5)
        while not pyw.isconnected(self.card):
            disp.warning("Waiting for connection to AP", ap.ssid)
            time.sleep(0.5)
        disp.info("Connected to network", ap.ssid)


    def disconnect(self):
        self.__check_mode(MODE_MAN)
        do("dhclient -r", self.card.dev)
        pyw.disconnect(self.card)
        disp.info("Wireless adapter", self.card.dev, "disconnected from any Access Point")


    def acquire_IP(self):
        self.__check_mode(MODE_MAN)

        if not pyw.isconnected(self.card):
            disp.error("Can't acquire IP using DHCP: wireless card not connected to AP!")
            return false
        else:
            do("dhclient -v", self.card.dev)
            return True


    def get_IP(self):
        return pyw.ifinfo(self.card)['inet']

