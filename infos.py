PRGNAME = "nctmenu"
VERSION = "0.20180816"

HOWTO = PRGNAME + """.py

Usage:
    """ + PRGNAME + """.py [options]

Options:
    -h, --help      This help.
    -r, --rescan    Recreate scanning files (ask scan executable directories,
                                             then scan given directories).
"""


# FIXME: Problème si plusieurs whatis trouvés.


import subprocess

def ask_info(file):
    """
    Parse the whatis of a file.
    @parameters : file = the file.
    @return : the whatis parsed.
    """
    try:
        info_str = subprocess.check_output(['whatis', '-l', '-s', '1:6:8', file],
                                           stderr=subprocess.STDOUT)\
                                          .decode('UTF-8')              # No encoding=something before Python3.5
        infoèstr = info_str.splitlines()
        info_str = info_str.split(" - ")[1].strip()
        info_str = info_str[0].upper() + info_str[1:]

    except subprocess.CalledProcessError as e:
        info_str = ""

    return info_str
