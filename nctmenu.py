#!/usr/bin/python3
# -*- coding: utf-8 -*-


# Standard library import.
import sys
import os
import argparse
import hashlib
import re

# Third-part library import.

# Project library import.
import infos

######################

def main(arg):
    """
    Main function.
    @parameters : some arguments, in case of use.
    @return : 0 = all was good.
              ... = some problem occures.
    """
    # check_args()
    # config ... <- Use Class()
    # verif_3rd_part_prg()
    # verif_exec_other_paths()
    # check_man_help ... <- Use Class()
    # check_gfx_version ... <- Use Class()
    # display()

    return 0

######################

if __name__ == "__main__":
    rc = main(sys.argv[1:])      # Keep only the argus after the script name.
    sys.exit(0)

