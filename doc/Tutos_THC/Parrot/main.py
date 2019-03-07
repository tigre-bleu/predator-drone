#! /usr/bin/env python3
#
# Scapy introduction tutorial in order to take control of a Parrot AR.Drone 2.0
#

from scapy.all import *
import subprocess as sbp
import sys, re


# ===============
#    Variables
# ===============

debug_sudo    = False

bssid_list    = []
clients_list  = []

WIFI_CHAN_MIN = 1
WIFI_CHAN_MAX = 12

PARROT_MACS   = ["90:03:b7", "00:12:1c", "90:3a:e6", "a0:14:3d", "00:12:1c", "00:26:7e"]



# =======================
#    Command execution
# =======================

def sudo(*args):
    """
    Execute an external command.

    :param args: The command line to be executed (can be a tuple)

    Examples:
        - sudo("ip link set", dev_name, "up")
        - sudo("ip link set "+dev_name+" up")
    """
    command     = ' '.join(args)

    try:
        if debug_sudo:
            print("Running '" + command + "'")
        p = sbp.Popen(command, shell=True, stderr=sys.stderr, stdout=sys.stdout)
        p.wait()

        if p.returncode < 0:
            print("Command '"+command+"' killed by signal", p.returncode)
        elif debug_sudo:
            print("Command returned", p.returncode)

    except OSError as e:
        print("Execution failed:", e)
        sys.exit(1)



# =================
#    APs listing
# =================

def filter_beacon(p):
    """ Filter beacon frames. """
    return p.haslayer(Dot11Beacon)


def print_ap(p):
    """ Print Access Point if not already printed. """
    global bssid_list

    # Retreive network statistics
    netstats = p[Dot11Beacon].network_stats()

    # Get AP details
    bssid    = p.addr3
    ssid     = netstats['ssid']
    channel  = netstats['channel']
    crypto   = netstats['crypto']

    # Print AP if not already printed
    if bssid not in bssid_list:
        # Register AP to not print it another time
        bssid_list.append(bssid)
        # Print AP
        print("AP", ssid, "("+bssid+")", "on channel", str(channel), "("+'/'.join(crypto)+")")
        # TODO partie 4


def list_ap(wlan):
    """ List Access Points. """
    # TODO partie 1
    sniff(iface=wlan, timeout=1, lfilter=filter_beacon, prn=print_ap)



# =====================
#    Clients listing
# =====================

def filter_clients(bssid, p):
    """ Filter wifi packets of a specific BSSID, sent from/to AP. """
    # Filter WiFi packets (Dot11FCS), with IP layer, on SSID bssid
    # TODO partie 2
    return False


def print_client(p):
    """ Register client of a specific BSSID. """
    global clients_list

    # Extract informations
    mac_dst = p.addr1
    mac_src = p.addr2
    bssid   = p.addr3

    ip_dst = p[IP].dst
    ip_src = p[IP].src

    # Compute client MAC and IP
    mac   = mac_src   if mac_src != bssid     else mac_dst
    ip    = ip_src    if mac_src != bssid     else ip_dst

    # Register client
    if mac not in clients_list:
        # Register client to not display it another time
        clients_list.append(mac)
        # Display client informations
        print("Client", mac, "with IP", ip)


def search_clients(wlan, bssid, channel):
    """ Search for clients. """
    # TODO partie 2
    print("TODO")



# ====================
#    Control taking
# ====================

def deauth_client(wlan, client_mac, bssid, channel):
    """ Deauthenticate client from AP. """
    # TODO partie 3
    print("TODO")



# ==================
#    Main program
# ==================

def is_mac(arg):
    """ Checks that a string is a MAC address. """
    return re.match('^([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}$', arg) != None


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)

    if argc == 3 and argv[2] == "-l":
        print("Listing available access points")
        list_ap(argv[1])

    elif argc == 5 and argv[2] == "-c":
        if not is_mac(argv[3]):
            print(argv[3], "is not a valid MAC address!")
        else:
            print("Listing connected clients for BSSID", argv[3], "on channel", argv[4])
            search_clients(argv[1], argv[3], argv[4])

    elif argc == 6 and argv[2] == "-d":
        if not is_mac(argv[3]):
            print(argv[3], "is not a valid MAC address!")
        elif not is_mac(argv[4]):
            print(argv[4], "is not a valid MAC address!")
        else:
            print("Disconnecting client", argv[3], "from BSSID", argv[4], "on channel", argv[5])
            deauth_client(argv[1], argv[3], argv[4], argv[5])

    else:
        print("Usage:")
        print("  ", argv[0], "<WLAN_ADAPTER> -l")
        print("  ", argv[0], "<WLAN_ADAPTER> -c <BSSID> <CHANNEL>")
        print("  ", argv[0], "<WLAN_ADAPTER> -d <CLIENT_MAC> <BSSID> <CHANNEL>")
        print("")
        print("   -l  List available Parrot APs")
        print("   -c  List connected clients to AP with MAC <BSSID> on channel <CHANNEL>")
        print("   -d  Disconnect client with MAC <CLIENT_MAC> from AP with MAC <BSSID>")
        print("       on channel <CHANNEL>")

