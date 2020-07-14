# -*- coding: utf-8 -*-

from .debug import *

# Standard libraries import.
import os
import pickle
import collections as c

# Third libraries import.

# Projet modules import.
from .infos import PRGNAME, ask_info
from . import scans

######################

FORBID_EXT = ['so',
              'a',
              'dll',
              'js',
              'png',
              'jpeg',
              'jpg',
              'gif',
              'doc',
              'docx'
              'odt'
              'odm',
              'xls',
              'xlsx',
            ]

######################

class Config():
    """
    Class used to configure program, and to create config files.

    Public attributes.
        found_bins : ordered and sorted dictionnary of found binaries files and their man/help/info.
    """

    # Private attributes.
        # __config_dir = Config. parent directory conventionnal.
        # __nctmenu_dir = Config. file it-self.
        # __prog_config_file = Program config file.
        # __bins_list_file = Found binaries' list.

        # __paths_to_scan = list of paths to scan to find binary files.

        # __exists_full_prog_conf_dir = Existing config directory flag.

        # __x_bins = binaries running under desktop.

    __DEFAULT = ['/bin', '/usr/bin', '/usr/local/bin', '/opt']

    # Public methods.

    def __init__(self, args):
        """
        __init__ : initiate class
        @parameters : args = the program arguments.
        @return : if something wrong, raise an OSError exception.
        """
#        self.found_bins = c.OrderedDict([('term',c.OrderedDict()),('x',c.OrderedDict())])
        self.found_bins = c.OrderedDict()

        self.__config_dir = os.path.expanduser("~") + os.sep + ".config" + os.sep
        self.__nctmenu_dir = PRGNAME + os.sep

        self.__prog_config_file = PRGNAME + ".conf"
        self.__bins_list_file = "bins.list"

        self.__exists_full_prog_conf_dir = os.path.exists(self.__config_dir + self.__nctmenu_dir + self.__bins_list_file)

        if not self.__exists_full_prog_conf_dir or "--rescan" in args:
            # Config from 0.
            self.__paths_to_scan = self.__DEFAULT # By default.
            if not self.__create_conf(self.__config_dir + self.__nctmenu_dir):
                raise FileNotFoundError("\n!!! Couldn't be created. Please check the parent directory rights or maybe already exists. !!!\n")

        if self.__exists_full_prog_conf_dir:
            # Read general config. and binaries list files.
            if not self.__recovering_gen_conf(self.__config_dir + self.__nctmenu_dir):
                raise FileNotFoundError("\n!!! {} has been unexpectly deleted! !!!\n".format(self.__prog_config_file))

            if not self.__recovering_bins_list(self.__config_dir + self.__nctmenu_dir):
                raise FileNotFoundError("\n!!! {} has been unexpectly deleted! !!!\n".format(self.__bins_list_file))

        # NOTE: debug
#        printthis("self.__config_dir", self.__config_dir)

    # Private methods.
    def __recovering_gen_conf(self, conf_dir):
        """
        Recover the general config.
        @parameters : conf_dir = directory where to create config's files.
        @return : True = all is ok.
        """
        print("{} exists. General conf. recovering ...".format(conf_dir))

        full_prog_conf_file = conf_dir + self.__prog_config_file

        # NOTE: debug
#        printthis("full_prog_conf_file", full_prog_conf_file)

        try:
            with open(full_prog_conf_file, "r+t") as f:
                self.__paths_to_scan = [line.strip() for line in f if line.find('/') > -1]

            print(self.__paths_to_scan)
        except:
            return False

        return True

    def __recovering_bins_list(self, conf_dir):
        """
        Recover the list of binairies.
        @parameters : conf_dir = directory where to create config's files.
        @return : True = all is ok.
        """
        print("{} exists. Binairies list recovering ...".format(conf_dir))

        full_bins_list_files = conf_dir + self.__bins_list_file

        # NOTE: debug
#        printthis("full_bins_list_files", full_bins_list_files)

        try:
            with open(full_bins_list_files, "r+b") as f:
                self.found_bins = pickle.load(f)
        except:
            return False

        # NOTE: debug
#        printthis("self.found_bins", self.found_bins)

        return True

    def __create_conf(self, conf_dir):
        """
        Create config directory and files if not exist or --rescan arg has been given.
        @parameters : conf_dir = directory where to create config's files.
        @result : True = all is ok.
        """
        if not os.path.exists(conf_dir):
            print("{} doesn't exist. Create ...".format(conf_dir))
            try:
                os.makedirs(conf_dir, mode=0o700)
                print("Created.\n")
            except OSError:
                return False

        full_prog_conf_file = conf_dir + self.__prog_config_file
        full_bins_list_files = conf_dir + self.__bins_list_file

        if not os.path.exists(full_prog_conf_file):
            print("{} doesn't exists. Create ...".format(full_prog_conf_file))
            with open(full_prog_conf_file, "w+t") as f:
                f.write("# {} #\n\n".format(self.__prog_config_file))
                f.write("# Default binaries paths -- Just add yours below with your lovely text editor #\n")
                for def_conf in self.__DEFAULT:
                    f.write("{}\n".format(def_conf))
        else:
            self.__recovering_gen_conf(conf_dir)  # To have binaries paths

        overwrite = "y"     # Overwrite by default.

        if os.path.exists(full_bins_list_files):
            overwrite = ""
            while overwrite not in ['y', 'n']:
                overwrite = input("{} exists. Create it again (y/n) : ".format(full_bins_list_files))
        else:
            print("{} doesn't exists. ".format(full_bins_list_files), end='')

        if overwrite == 'y':
            print("Creating ...")

            # Search for programs running inside X.
            # TODO: commmentaire à effacer à MàP
#            self.__x_bins = sorted([f for f in scans.scan_for_X_binfiles()])
            self.__x_bins = [f for f in scans.scan_for_X_binfiles()]

            # 1st scans binary files in given paths.
            self.found_bins = c.OrderedDict([(k, '') for k in scans.scan_for_binfiles(self.__paths_to_scan)])
            # TODO: commmentaire à effacer à MàP
            # And order them according their directory.
#            self.found_bins = c.OrderedDict(sorted(self.found_bins.items(), key=lambda t: t[0]))

            # XFree or terminal program ?
            # Looking for informations about each binaries.
            l = len(self.found_bins)    # Prepare percentage.
            print("\n\tSearching informations about {} found files...\n".format(l), end='')
            cpt = 0
            percent = 0
            oldpercent = -1

            for binfile in self.found_bins.keys():

                mode = 'x' if binfile.split('/').pop() in self.__x_bins else 'term'

                # Ask for informations about a binary.
                self.found_bins[binfile] = (ask_info(binfile), mode)

                percent = int(cpt / l * 100)
                if percent > oldpercent and percent % 10 == 0:
                    print("\t{}%".format(percent))
                    oldpercent = percent

                cpt += 1

            print("\t100%")

            # Save in file.
            with open(full_bins_list_files, "w+b") as f:
                p = pickle.dump(self.found_bins, f)

            print("Created.\n")

        return True

######################

if __name__ == "__main__":
    help(Config)
