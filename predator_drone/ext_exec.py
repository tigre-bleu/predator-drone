#
# External command execution
#

import subprocess as sbp
from . import disp
import sys


def do(*args, force_output=False):
    """ Execute an external command. """
    command     = ' '.join(args)
    show_output = disp.Verb.isdebug() or force_output

    try:
        disp.debug("Running '" + command + "'")
        p = sbp.Popen(command, shell=True, stderr=sys.stderr,
                stdout=(sys.stdout if show_output else sbp.DEVNULL))
        p.wait()

        if p.returncode < 0:
            disp.die("Command killed by signal", p.returncode)
        else:
            disp.debug("Command returned", p.returncode)

    except OSError as e:
        disp.error("Execution failed:", e)


def sudo(*args, force_output=False):
    """ Execute a sudo command. """
    do("sudo", *args, force_output=force_output)

