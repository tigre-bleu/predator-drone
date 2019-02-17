#! /usr/bin/env python3
#
# Display management
#

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

class syms:
    ERROR = term.RED    + term.BOLD + "/!\\"  + term.ENDC
    WARN  = term.ORANGE + term.BOLD + "/!\\"  + term.ENDC
    DBG   = term.BLUE   + term.BOLD + "-->"   + term.ENDC
    INFO  = term.GREEN  + term.BOLD + "==>"   + term.ENDC
    LIST0 = term.GREEN  + term.BOLD + " -"    + term.ENDC
    LIST1 = term.GREEN  + term.BOLD + "    -" + term.ENDC


def join(msg):
    """ Builds a string from a tuple. """
    if isinstance(msg, str):
        return msg
    else:
        return ' '.join(msg)


def todo(*msg):
    """ Prints a TODO message. """
    print(term.ORANGE + term.BOLD + "TODO:" + term.ENDC + term.ORANGE, *msg, term.ENDC)


def banner(banner):
    """ Prints the program banner. """
    print(term.CLEAR + term.BLUE + banner + term.ENDC)



def error(*msg):
    """ Prints an error message. """
    print(syms.ERROR + term.RED + term.BOLD, *msg, term.ENDC)


def warn(*msg):
    """ Prints a warning message. """
    print(syms.WARN, *msg)


def debug(*msg):
    """ Prints debugging message. """
    print(syms.DBG, *msg)


def info(*msg):
    """ Prints info message. """
    print(syms.INFO, *msg)


def item0(*msg):
    """ Prints a first level item (of a list). """
    print(syms.LIST0, *msg)


def item1(*msg):
    """ Prints a second level item (of a list). """
    print(syms.LIST1, *msg)


def menu_title(title):
    """ Prints a menu title. """
    print('\n' + term.PURPLE
            + "================================================================================"
            + term.ENDC + '\n\n'
            + term.BOLD + title + term.ENDC)


def menu_option(char, msg):
    """ Prints a menu option. """
    print("  [" + term.ORANGE + term.BOLD + char + term.ENDC + "]", msg)
