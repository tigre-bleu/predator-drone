#! /usr/bin/env python3
#
# Drone hacking tool
#

from argparse import ArgumentParser
from predator_drone import *
import sys, os


# ======================
#    Useful functions
# ======================

def usage():
    print("Usage:", sys.argv[0], " [-v <verb-level>] iface mon_iface")
    print("  iface        will be the wireless interface used to connect to Parrot AR.Drone")
    print("  mon_iface    will be the monitoring wireless interface")
    print("  <verb-level> between", disp.Verb.ERROR, "and", disp.Verb.DEBUG)
    print("     ", disp.Verb.ERROR,   "= ERROR")
    print("     ", disp.Verb.WARNING, "= WARNING")
    print("     ", disp.Verb.INFO,    "= INFO")
    print("     ", disp.Verb.DEBUG,   "= DEBUG")
    sys.exit(0)


def clear_lists(menu, parrot, syma):
    """ Clears all lists (registered APs, etc.). """
    menu.clear_numbered_opt()
    parrot.clear_lists()
    syma.clear_lists()



# ==================
#    Main program
# ==================

if __name__ == "__main__":

    # Check root access
    if os.geteuid() != 0:
        disp.die("Please run this script as root!")


    # Parse arguments
    iface     = ""
    mon_iface = ""
    argc = len(sys.argv)

    try:
        if argc == 3:
            iface     = sys.argv[1]
            mon_iface = sys.argv[2]

        elif argc == 5 and sys.argv[1] == "-v":
            verb_lvl = int(sys.argv[2])
            if disp.Verb.ERROR <= verb_lvl <= disp.Verb.DEBUG:
                disp.Verb.curr = verb_lvl
                iface          = sys.argv[3]
                mon_iface      = sys.argv[4]
            else:
                raise Exception
        else:
            raise Exception
    except:
        usage()


    # Check that the two interfaces are differents
    if iface == mon_iface:
        disp.die("The monitoring interface and managed one must be different!")


    # Hacking tools
    #  - Parrot
    wifi_mon = WifiManager(mon_iface, mon_mode=True)
    wifi     = WifiManager(iface,     mon_mode=False)
    parrot_list = ParrotAPsList(wifi, wifi_mon)
    #  - Syma X5C-1
    syma_list = SymaScanner()


    # Display banner
    disp.banner(
            "      ____                                               __      __            \n"
            "     / __ \_________  ____  ___     ____  ________  ____/ /___ _/ /_____  _____\n"
            "    / / / / ___/ __ \/ __ \/ _ \   / __ \/ ___/ _ \/ __  / __ `/ __/ __ \/ ___/\n"
            "   / /_/ / /  / /_/ / / / /  __/  / /_/ / /  /  __/ /_/ / /_/ / /_/ /_/ / /    \n"
            "  /_____/_/   \____/_/ /_/\___/  / .___/_/   \___/\__,_/\__,_/\__/\____/_/     \n"
            "                                /_/                                            \n")


    # Main menu
    main_menu = Menu("Main menu:", "Your choice:",
            exit_opt_msg  ="Exit program",
            no_num_opts_msg="No drone detected. Try to refresh!")

    main_menu.add_static_opt('P', "Parrot AR.Drone2 :: Refresh Parrot APs list",
            lambda: parrot_list.refresh_aps_list(main_menu))
    main_menu.add_static_opt('W', "Parrot AR.Drone2 :: Show found Access Points",
            parrot_list.show_detected_aps)

    main_menu.add_static_opt('X', "Syma X5C-1 drone :: Scan RF for drones",
            lambda: syma_list.scan(main_menu))
    main_menu.add_static_opt('D', "Syma X5C-1 drone :: Show detected drones",
            syma_list.show_detected_drones)

    main_menu.add_static_opt('C', "Clear all lists",
            lambda: clear_lists(main_menu, parrot_list))

    main_menu.run()

