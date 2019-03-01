#
# External command execution
#

import subprocess as sbp
from . import disp
import sys


def do(*args, force_output=False, get_output=False):
    """ Execute an external command. """
    command     = ' '.join(args)
    show_output = disp.Verb.isdebug() or force_output

    try:
        disp.debug("Running '" + command + "'")
        if not get_output:
            p = sbp.Popen(command, shell=True, stderr=sys.stderr,
                    stdout=(sys.stdout if show_output else sbp.DEVNULL))
            p.wait()
        else:
            p = sbp.Popen(command, shell=True, stderr=sbp.STDOUT, stdout=sbp.PIPE)
            (output, _) = p.communicate()
            p.wait()
            return output.decode()

        if p.returncode < 0:
            disp.die("Command killed by signal", p.returncode)
        else:
            disp.debug("Command returned", p.returncode)

    except OSError as e:
        disp.error("Execution failed:", e)

