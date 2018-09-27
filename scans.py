# -*- coding: utf-8 -*-

# Standard libraries import.
import os
import subprocess
# TODO: A enlever après MàP #############################
import pickle
# #######################################################

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
        @parameters : ...
        @return : none.
        """
        self.__exists_locate = self.__existing_locate()
        if not self.__exists_locate:
#            self.updatedb_emul()
            self.locate_cmd = self.locate_emul

        else:
            self.locate_cmd = self.locate_real

    def updatedb_emul(self):
        """
        Emulation of updatedb command.
        @parameters : none.
        @return : none.
        """
        print("\nupdatedb or locate command not found. Suppose the package hasn't been installed.")
        print("\tUse emulation of updatedb/locate.")
        print("\tScan disk to find .desktop. Please, waiiit.")

        # TODO: Revenir à la recherche locate_real à partir de / après MaP

        config_dir = os.path.expanduser("~") + os.sep + ".config" + os.sep
        nctmenu_dir = "nctmenu" + os.sep
        tmp_list_nf = config_dir + nctmenu_dir + "updatedb.lst"
        if not os.path.exists(tmp_list_nf):
            print("Recherche et enregistrement")
            cmd = "find / \( -name *.desktop -o -name *.Desktop \) -exec echo 2>/dev/null {} \;"
            self.__found_files = subprocess.getoutput(cmd).splitlines()

            with open(tmp_list_nf, "w+b") as f:
                pickle.dump(self.__found_files, f)

    def locate_emul(self):
        """
        Generator : emulation of locate command.
        @parameters : none.
        @return : yield a file name in .desktop. If something wrong, return False.
        """
        print("\nlocate_emul()")

        config_dir = os.path.expanduser("~") + os.sep + ".config" + os.sep
        nctmenu_dir = "nctmenu" + os.sep
        tmp_list_nf = config_dir + nctmenu_dir + "updatedb.lst"

        try:
            with open(tmp_list_nf, "r+b") as f:
                self.__found_files = pickle.load(f)

        except:
            print('updatedb.lst file not found !')
            return False

#        print(self.__found_files)
        for ff in self.__found_files:
            yield ff

    def locate_real(self):
        """
        Generator : use real updatedb.
        @parameters : none.
        @return : yield a file name in .desktop.
        """
        print("\nlocate_real()")
        cmd = "mlocate -i *.Desktop"
        for ff in subprocess.getoutput(cmd).splitlines():
            yield ff

#        self.__found_files = subprocess.getoutput(cmd).splitlines()
#        print(self.__found_files)

    def __existing_locate(self):
        """
        Search if updatedb and locate commands are present.
        @parameters : none.
        @return : True if exists.
        """
        return False    # TODO: À effacer après MaP.

        # Best universal way to know if a command exists. Maybe ?
        # Remember for shell >0 means NOK.
        if subprocess.getstatusoutput("whatis mlocate")[0]:
            return False

        if subprocess.getstatusoutput("whatis updatedb")[0]:
            return False

        return True


    # Private methods.

######################

def scan_for_binfiles(paths):
    """
    Generator : find binaries.
    @parameters : paths = paths where to try to find binaries.
    @return : the binary.
    """
#        print(paths)
    for path in paths:
        print("\tScanning", path)
        # fwalk help recipe.
        for root, dirs, files, rootfd in os.fwalk(path):
            for file in files:
                try:    # Maybe a file will raise a problem.
                    if os.stat(file, dir_fd=rootfd).st_mode & 0o111 == 0o111:  # UGO +x ?
                        yield os.path.join(path, file)

                except:     # Problem with a file ? Don't care about !
                    continue


def scan_for_X_binfiles():
    """
    Generator : scan binaries running under X, finding .desktop ones.
    @parameters :
    @return :
    """
    mlocate_emul = Mlocate_emul()
    mlocate_emul.locate_cmd()

######################

if __name__ == "__main__":
    print("Don't use me directely.")
