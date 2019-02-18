#! /usr/bin/env python3
#
# Drone hacker tool
# Inspired from https://github.com/samyk/skyjack/
#

from parrot_list import ParrotAPsList
from wifi import WifiManager
from menu import Menu
import argparse
import disp



# ======================
#    Useful functions
# ======================

def clear_lists(menu, parrot_hacker):
    """ Clears all lists (registered APs, etc.). """

    menu.clear_numbered_opt()
    disp.info("Numbered entries of main menu cleared")

    parrot_hacker.clear_lists()
    disp.info("Access Points lists cleared")



# ==================
#    Main program
# ==================

if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description="Drone predator")
    parser.add_argument("--verb", "-v", type=int, default=disp.Verb.INFO,
            help="script verbosity (0,.. => ERROR, WARNING, INFO, DEBUG)")
    args = parser.parse_args()

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
    parrot_list = ParrotAPsList(WifiManager("wlp61s0", "phy0"))

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

