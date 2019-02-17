#! /usr/bin/env python3
#
# Drone hacker tool
# Inspired from https://github.com/samyk/skyjack/
#

from menu import Menu
import disp


# ===============
#    Main code
# ===============

if __name__ == "__main__":
    disp.banner(
            "      ____                                               __      __            \n"
            "     / __ \_________  ____  ___     ____  ________  ____/ /___ _/ /_____  _____\n"
            "    / / / / ___/ __ \/ __ \/ _ \   / __ \/ ___/ _ \/ __  / __ `/ __/ __ \/ ___/\n"
            "   / /_/ / /  / /_/ / / / /  __/  / /_/ / /  /  __/ /_/ / /_/ / /_/ /_/ / /    \n"
            "  /_____/_/   \____/_/ /_/\___/  / .___/_/   \___/\__,_/\__,_/\__/\____/_/     \n"
            "                                /_/                                            \n")

    main_menu = Menu("Main menu:", "Your choice:",
            exit_msg="Exit program",
            no_numbered_opts_msg="No Parrot AP detected. Try to refresh!")
    main_menu.add_static_opt('R', "Refresh running APs and Parrot APs", lambda: disp.todo("Refresh APs"))
    main_menu.add_static_opt('S', "Show found APs", lambda: disp.todo("Show APs"))
    main_menu.run()

    # for i in range(0, parrot_count):
    #     ap = parrot_aps[i]
    #     print_menu_opt(str(i+1), "Hack Parrot", ap.ssid, '(' + ap.bssid + ')')

