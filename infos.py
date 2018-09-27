PRGNAME = "nctmenu"
VERSION = "0.20180816"

HOWTO = PRGNAME + """.py

Usage:
    """ + PRGNAME + """.py [options]

Options:
    -h, --help      This help.
    -r, --reconf    Recreate configuration file (ask scan executable directories,
                                                 then scan given directories).
    -d, --dummy     Dummy option.
"""


import subprocess

def ask_info(file):
    """
    Parse the whatis of a file.
    @parameters : file = the file.
    @return : the whatis parsed.
    """
#        print("Info about {}".format(file))

    try:
        info_str = subprocess.check_output(['whatis', '-l', '-s', '1:4:5:6:7:8:9', file],
                                           stderr=subprocess.STDOUT)\
                                          .decode('UTF-8')              # No encoding=something before Python3.5
        info_str = info_str.split("-")[1].strip()

    except subprocess.CalledProcessError as e:
        info_str = ""

    return info_str
