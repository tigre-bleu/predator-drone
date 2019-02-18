#! /usr/bin/env python3
#
# Parrot APs listing functions
#

from wifi import WifiManager, AccessPoint
from parrot_hack import ParrotHacker
import disp
import re



# ========================
#    Parrot APs listing
# ========================

class ParrotAPsList:
    # Parrot owns the 90:03:B7 block of MACs and a few others
    # see here: http://standards.ieee.org/develop/regauth/oui/oui.txt
    PARROT_MACS = ("90:03:B7", "00:12:1C", "90:3A:E6", "A0:14:3D", "00:12:1C", "00:26:7E")


    def __init__(self, wlan):
        """
        Initialize the Parrot APs listing class.

        : param wlan  A WifiManager instance, to manipulate WiFi
        """
        self.wlan = wlan

        self.parrot_aps     = []
        self.parrot_hackers = []



    # =========================
    #    APs listing methods
    # =========================

    def refresh_aps_list(self, menu):
        """
        Refresh APs list.

        : param menu  A Menu instance in which add Parrot APs
        """
        self.wlan.refresh_aps_list()

        # Filter Parrot's MAC addresses
        disp.info("Filtering Parrot's APs")
        for ap in self.wlan.detected_aps:
            # Eventually register AP only if not registered
            if ap not in self.parrot_aps:
                # Check all Parrot MACs
                for mac in self.PARROT_MACS:
                    if re.match(mac, ap.bssid, re.IGNORECASE):
                        hacker = ParrotHacker(self.wlan, ap)
                        self.parrot_hackers.append(hacker)

                        menu.add_numbered_opt( ("Hack Parrot", ap.ssid, '(' + ap.bssid + ')'),
                                                hacker.hack)

                        disp.item1("New Parrot drone found with MAC", ap.bssid)


    def show_detected_aps(self):
        """ Show detected access points. """
        self.wlan.show_detected_aps()

        # Show Parrot APs
        print("Found APs with Parrot MAC address:")
        if len(self.parrot_hackers) == 0:
            disp.item0(disp.red("No Parrot AP found!"))
        else:
            for hacker in self.parrot_hackers: disp.item0(hacker)


    def clear_lists(self):
        """ Clears APs lists. """
        self.parrot_hackers = []
        self.wlan.clear_aps_list()

