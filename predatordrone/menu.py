#! /usr/bin/env python3
#
# Menu made easy!
#

import predatordrone.disp as disp
import sys


# =======================
#    Option management
# =======================

class Option:
    def __init__(self, msg, fct):
        """
        Instantiates a menu option.
        
        : param msg     The option description (tuple or str)
        : param fct     The function to call when this option is selected
        """
        self.msg = disp.join(msg)
        self.fct = fct

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__



# =====================
#    Menu management
# =====================

class Menu:
    def __init__(self, title, question, exit_opt_msg="Exit this menu",
            no_num_opts_msg="", exit_on_ctrlc=True):
        """
        Creates a menu.

        : param title           The menu title (tuple or str)
        : param question        The question to invite user input (tuple or str)
        : param exit_opt_msg    The message for exit option (tuple or str)
        : param no_num_opts_msg The message shown if there are no numbered options
        : param exit_on_ctrlc   Specify whether the menu exits on CTRL+C

        Note: the option 'Q' will always exit the menu
        """
        self.title           = disp.join(title)
        self.numbered_opts   = {}
        self.static_opts     = {}
        self.question        = disp.join(question)
        self.no_num_opts_msg = disp.join(no_num_opts_msg)
        self.exit_on_ctrlc   = exit_on_ctrlc

        self.add_static_opt('Q', exit_opt_msg, self.__exit)



    # =====================
    #    Running methods
    # =====================

    def run(self):
        """ Runs the menu: showing it, then capturing user input. """
        self.stop = False
        while not self.stop:
            try:
                # Build option list
                all_options = dict(self.static_opts)
                all_options.update(self.numbered_opts)

                # Show menu
                self.__print_menu_title()
                self.__print_numbered_opts()
                self.__print_static_opts()

                # Get user input
                user_input = input('\n' + self.question + ' ').upper()

                # Exec user action
                print()
                all_options[user_input].fct()

            except KeyError as e:
                disp.error(e, "is not an option!")

            except KeyboardInterrupt:
                print()
                if self.exit_on_ctrlc:
                    self.__exit()

            except EOFError:
                print()
                sys.exit(0)


    def __exit(self):
        """ Exits the menu. """
        self.stop = True



    # =================================
    #    Numbered options management
    # =================================

    def clear_numbered_opt(self):
        """ Clears the registered number options. """
        self.numbered_opts = {}


    def add_numbered_opt(self, msg, fct):
        """
        Adds a numbered option to the current menu.
        
        : param msg     Option explanation (tuple or str)
        : param fct     Function to be executed when the option is selected
        """
        idx = len(self.numbered_opts)
        self.numbered_opts[str(idx)] = Option(msg, fct)



    # ===============================
    #    Static options management
    # ===============================

    def add_static_opt(self, char, msg, fct):
        """
        Adds a static option to the current menu.
        
        : param char    Option character
        : param msg     Option explanation (tuple or str)
        : param fct     Function to be executed when the option is selected
        """
        self.static_opts[char.upper()] = Option(msg, fct)



    # ======================
    #    Printing methods
    # ======================

    def __print_menu_title(self):
        """ Prints menu title. """
        disp.menu_title(self.title)


    def __print_numbered_opts(self):
        """ Prints numbered menu options. """
        # Print numbered options if there are
        if len(self.numbered_opts) > 0:
            for str_idx in sorted(self.numbered_opts):
                option = self.numbered_opts[str_idx]
                disp.menu_option(str_idx, option.msg)

        # Else, print a missing message
        elif self.no_num_opts_msg != "":
            disp.menu_option(' ', self.no_num_opts_msg)


    def __print_static_opts(self):
        """ Prints static menu options. """
        # Print static options
        for char in self.static_opts:
            if char != 'Q':
                option = self.static_opts[char]
                disp.menu_option(char, option.msg)

        # Print exit option
        disp.menu_option('Q', self.static_opts['Q'].msg)

