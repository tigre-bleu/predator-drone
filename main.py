#! /usr/bin/env python3
#
# Drone hacker tool
#

from argparse import ArgumentParser
from predator_drone import *


# ======================
#    Useful functions
# ======================

def clear_lists(menu, parrot_hacker):
    """ Clears all lists (registered APs, etc.). """

    menu.clear_numbered_opt()
    disp.info("Main menu entries cleared")

    parrot_hacker.clear_lists()
    disp.info("Access Points lists cleared")



# ==================
#    Main program
# ==================

if __name__ == "__main__":

    # Parse arguments
    parser = ArgumentParser(description="Drone predator")
    parser.add_argument("--verb", "-v", type=int, default=disp.Verb.INFO,
            help="script verbosity (0,.. => ERROR, WARNING, INFO, DEBUG)")
    parser.add_argument("iface", type=str, default="",
            help="wireless interface to be used to connect to Parrot")
    parser.add_argument("mon_iface", type=str, default="",
            help="wireless interface to be used in monitoring mode")
    args = parser.parse_args()


    # Check that the two interfaces are differents
    if args.iface == args.mon_iface:
        disp.die("The monitoring interface and managed one must be different!")

    # Register verbosity
    disp.Verb.curr = args.verb


    # Display banner
    disp.banner(
            "      ____                                               __      __            \n"
            "     / __ \_________  ____  ___     ____  ________  ____/ /___ _/ /_____  _____\n"
            "    / / / / ___/ __ \/ __ \/ _ \   / __ \/ ___/ _ \/ __  / __ `/ __/ __ \/ ___/\n"
            "   / /_/ / /  / /_/ / / / /  __/  / /_/ / /  /  __/ /_/ / /_/ / /_/ /_/ / /    \n"
            "  /_____/_/   \____/_/ /_/\___/  / .___/_/   \___/\__,_/\__,_/\__/\____/_/     \n"
            "                                /_/                                            \n")


    # Hacking tools
    wifi_mon = WifiManager(args.mon_iface, mon_mode=True)
    wifi     = WifiManager(args.iface,     mon_mode=False)
    parrot_list = ParrotAPsList(wifi, wifi_mon)


    # Main menu
    main_menu = Menu("Main menu:", "Your choice:",
            exit_opt_msg  ="Exit program",
            no_num_opts_msg="No Parrot AP detected. Try to refresh!")

    main_menu.add_static_opt('R', "Refresh Parrot APs list",
            lambda: parrot_list.refresh_aps_list(main_menu))
    main_menu.add_static_opt('S', "Show found APs",
            parrot_list.show_detected_aps)
    main_menu.add_static_opt('C', "Clear all lists",
            lambda: clear_lists(main_menu, parrot_list))

    main_menu.run()

