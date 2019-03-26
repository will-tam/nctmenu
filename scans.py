# -*- coding: utf-8 -*-

from debug import *

# Standard libraries import.
import os
import subprocess
import re
import pickle

# Third libraries import.


# Projet modules import.


######################

class Mlocate_emul():
    """
    If no mlocate package on system, emulate both of most important utils in it.
    updatedb (<- advantage : don't need to be root)
    locate

    Public attributes.
        locate_cmd : which locate command to use.
    """

    # Private attributes.
    # __exists_locate = True if locate command exists, everelse False.

    # Public methods.

    def __init__(self):
        """
        __init__ : initiate class
        @parameters : none.
        @return : none.
        """
        self.__exists_locate = self.__existing_locate()
        if not self.__exists_locate:
            self.updatedb_emul()
            self.locate_cmd = self.locate_emul

        else:
            self.locate_cmd = self.locate_real

    def updatedb_emul(self):
        """
        Emulation of updatedb command.
        @parameters : none.
        @return : none.
        """
        print("\nupdatedb or mlocate command not found. Suppose the package hasn't been installed.")
        print("\tUse emulation of updatedb/locate.")

        config_dir = os.path.expanduser("~") + os.sep + ".config" + os.sep
        nctmenu_dir = "nctmenu" + os.sep
        tmp_list_nf = config_dir + nctmenu_dir + "updatedb.lst"
        if not os.path.exists(tmp_list_nf):
            print("\tupdatedb.lst doesn't exist. Scan disk to find .desktop. Please, waiiit.")
            cmd = "find / \( -name *.desktop -o -name *.Desktop \) -exec echo 2>/dev/null {} \;"
            self.__found_files = subprocess.getoutput(cmd).splitlines()

            with open(tmp_list_nf, "w+b") as f:
                pickle.dump(self.__found_files, f)
        else:
            print("\tupdatedb.lst allready exists. No scan needs, nice !")

    def locate_emul(self):
        """
        Generator : emulation of locate command.
        @parameters : none.
        @return : yield a file name in .desktop. If something wrong, return nothing !
        """
        config_dir = os.path.expanduser("~") + os.sep + ".config" + os.sep
        nctmenu_dir = "nctmenu" + os.sep
        tmp_list_nf = config_dir + nctmenu_dir + "updatedb.lst"

        try:
            with open(tmp_list_nf, "r+b") as f:
                self.__found_files = pickle.load(f)

            for ff in self.__found_files:
                yield ff

        except IOError:
            print('\n!! updatedb.lst file not found !!\n')

        except KeyboardInterrupt:
            return False

    def locate_real(self):
        """
        Generator : use real updatedb.
        @parameters : none.
        @return : yield a file name in .desktop.
        """
        cmd = "mlocate -i *.Desktop"
        for ff in subprocess.getoutput(cmd).splitlines():
            yield ff

#        self.__found_files = subprocess.getoutput(cmd).splitlines()
        # NOTE: debug
#        printthis("self.__found_file", self.__found_files)

    def __existing_locate(self):
        """
        Search if updatedb and locate commands are present.
        @parameters : none.
        @return : True if exists.
        """

        # TODO: Revenir à la recherche locate_real à partir de / après MaP
#        return False    # TODO: À effacer après MaP.

        # Best universal way to know if a command exists. Maybe ?
        # Remember for shell >0 means NOK.
        if subprocess.getstatusoutput("whatis mlocate")[0]:
            print("Sorry, no binary mlocate found !")
            return False

        if subprocess.getstatusoutput("whatis updatedb")[0]:
            print("Sorry, no binary updatedb found !")
            return False

        if subprocess.getoutput('find /var/lib/mlocate -name mlocate.dbz'):
            print("Sorry, no file mlocate.db found !")
            return False

        return True

    # Private methods.

######################

def scan_for_binfiles(paths):
    """
    Generator : find binaries.
    @parameters : paths = paths where to try to find binaries.
    @return : yield the binary.
    """
    # NOTE: debug
#    printthis("paths", paths)
    for path in paths:
        print("\tScanning", path)
        # fwalk help recipe.
        for root, dirs, files, rootfd in os.fwalk(path):
            for file in files:
                try:    # Maybe a file will raise a problem.
                    if os.stat(file, dir_fd=rootfd).st_mode & 0o111 == 0o111:  # UGO +x ?
                        yield os.path.join(root, file)

                except:     # Problem with a file ? Don't care about !
                    continue

def scan_for_X_binfiles():
    """
    Generator : scan binaries running under X, finding .desktop ones.
    Use freedesktop.org spec.
    @parameters : none.
    @return : yield the binaries running under X.
    """
    re_term = re.compile(r'^terminal=true', re.MULTILINE | re.I)
    re_exec = re.compile(r'(^exec=)(.*)', re.MULTILINE | re.I)
    re_opt = re.compile(r'\s-+|\s%?')

    def searchin(file):     # Faster than grep command.
        with open(file, "rt") as f:
            lines = f.read(-1)

        if re_term.search(lines):
            return False, ""

        rst = re_exec.search(lines)
        if rst:
            return True, rst.group(2)

        return False, ""

    mlocate_emul = Mlocate_emul()
    # NOTE: debug
#    printthis("mlocate_emul.locate_cmd", mlocate_emul.locate_cmd)
    for file in mlocate_emul.locate_cmd():
        cr, find = searchin(file)

        if cr and find:     # Beward of bad formated files.
            find = find.split('=').pop()
            find = re_opt.split(find)
            if find[0] in ['yes', 'true', 'false', 'sh', 'bash', 'ksh', 'csh']:
                find = find.pop()
            else:
                find = find[0]
            find = find.strip('"')
            find = find.strip("'")
            find = find.split('/').pop()
            yield find

######################

if __name__ == "__main__":
    print("Don't use me directely.")
