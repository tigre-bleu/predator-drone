#
# Display management
#

import sys


# ======================
#    Printing symbols
# ======================

class term:
    BLUE      = '\033[94m'
    GREEN     = '\033[92m'
    ORANGE    = '\033[93m'
    RED       = '\033[91m'
    PURPLE    = '\033[95m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
    EMPTY     = '\033c'
    CLEAR     = "\x1b[2J\x1b[H"

class syms:
    ERROR = term.RED    + term.BOLD + "/!\\"  + term.ENDC
    WARN  = term.ORANGE + term.BOLD + "/!\\"  + term.ENDC
    DBG   = term.BLUE   + term.BOLD + "-->"   + term.ENDC
    INFO  = term.GREEN  + term.BOLD + "==>"   + term.ENDC
    LIST0 = term.GREEN  + term.BOLD + "  -"   + term.ENDC
    LIST1 = term.GREEN  + term.BOLD + "    -" + term.ENDC




# ======================
#    String utilities
# ======================

def str_join(msg):
    """ Builds a string from a tuple. """
    if isinstance(msg, str):
        return msg
    else:
        return ' '.join(msg)

def str_red(*msg):
    """ Builds a red string from a tuple/str. """
    return term.RED + str_join(*msg) + term.ENDC




# =============================================
#    Message printing according to verbosity
# =============================================

class Verb:
    curr    = 2
    ERROR   = 0
    WARNING = 1
    INFO    = 2
    DEBUG   = 3

    def iserror():
        return True

    def iswarning():
        return Verb.curr >= Verb.WARNING

    def isinfo():
        return Verb.curr >= Verb.INFO

    def isdebug():
        return Verb.curr >= Verb.DEBUG


def die(*msg):
    """ Prints an error message then exit. """
    error(*msg)
    sys.exit(1)


def error(*msg):
    """ Prints an error message. """
    if Verb.iserror():
        print(syms.ERROR + term.RED + term.BOLD, *msg, term.ENDC)


def warn(*msg):
    """ Prints a warning message. """
    if Verb.iswarning():
        print(syms.WARN, *msg)


def info(*msg):
    """ Prints info message. """
    if Verb.isinfo():
        print(syms.INFO, *msg)


def debug(*msg):
    """ Prints debugging message. """
    if Verb.isdebug():
        print(syms.DBG, *msg)




# ======================
#    Message printing
# ======================

def banner(banner):
    """ Prints the program banner. """
    print(term.CLEAR + banner + term.ENDC)


def todo(*msg):
    """ Prints a TODO message. """
    print(term.ORANGE + term.BOLD + "TODO:" + term.ENDC + term.ORANGE, *msg, term.ENDC)


def item0(*msg):
    """ Prints a first level item (of a list). """
    print(syms.LIST0, *msg)


def item1(*msg):
    """ Prints a second level item (of a list). """
    print(syms.LIST1, *msg)




# ===================
#    Menu printing
# ===================

def menu_title(title):
    """ Prints a menu title. """
    print('\n' + term.PURPLE
            + "================================================================================"
            + term.ENDC + '\n\n'
            + term.BOLD + title + term.ENDC)


def menu_option(char, msg):
    """ Prints a menu option. """
    print("  [" + term.ORANGE + term.BOLD + char + term.ENDC + "]", msg)

