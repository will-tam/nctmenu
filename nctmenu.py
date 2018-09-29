#!/usr/bin/python3
# -*- coding: utf-8 -*-

from debug import *

# Standard library import.
import sys
import os
import argparse
import hashlib
import re

# Third-part library import.
import docopt

# Project library import.
import infos
import config

######################

def main(args):
    """
    Main function.
    @parameters : some arguments, in case of use.
    @return : 0 = all was good.
              ... = some problem occures.
    """
#    conf = config.Config([c[0] for c in args.items() if c[1]])
    try:
        conf = config.Config([c[0] for c in args.items() if c[1]])
        # NOTE: debug
#        printthis("conf.found_bins", conf.found_bins)
    except BaseException as e:
        print("\n{}".format(e))
        return 1

    # verif_3rd_part_prg()
    # verif_exec_other_paths()
    # check_man_help ... <- Use Class()
    # check_gfx_version ... <- Use Class()
    # display()

    return 0

######################

if __name__ == "__main__":
    args = docopt.docopt(infos.HOWTO, help=True)
    rc = main(args)      # Keep only the argus after the script name.
    sys.exit(rc)

