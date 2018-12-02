#!/usr/bin/python3
# -*- coding: utf-8 -*-

from debug import *

# Standard library import.
import sys
import os
import argparse
import hashlib
import re
import curses
import subprocess

import collections as c

# Third-part library import.
import docopt

# Project library import.
import infos
import config
import nctm_display

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

    # NOTE: debug
#    printthis("conf.found_bins", conf.found_bins)

    # NOTE: debug
#    for i, v in enumerate([k for k in conf.found_bins.keys()]):
#        print("{} - {} -> {}".format(i, v, conf.found_bins[v][0]))

#    def find_name(absolute):
#        only_name = absolute[0].split("/")
#        return only_name[-1]

#    f = conf.found_bins
#    f = c.OrderedDict(sorted(f.items(), key=lambda t: find_name(t)))
#    conf.found_bins = f

#    f = sortacc.Sorted_according().pathes(conf.found_bins)
#    f = sortacc.Sorted_according().filenames(conf.found_bins)
#    f = sortacc.Sorted_according().documentations_exist(conf.found_bins)
#    for i, v in enumerate(f.items()):
#        print("{} - {} -> {}".format(i, v, v[1]))

    curses.wrapper(nctm_display.NCTM_Display, conf)

    return 0

######################

if __name__ == "__main__":
    args = docopt.docopt(infos.HOWTO, help=True)
    rc = main(args)      # Keep only the argus after the script name.
    sys.exit(rc)
