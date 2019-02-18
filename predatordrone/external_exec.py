#! /usr/bin/env python3
#
# External command execution
#

import predatordrone.disp as disp
import subprocess as sbp
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

        if p.returncode != 0:
            disp.error("Command failed with exit code", p.returncode)
            sys.exit(1)
        else:
            disp.debug("Command returned", p.returncode)

    except OSError as e:
        disp.error("Execution failed:", e)

