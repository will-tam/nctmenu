# -*- coding: utf-8 -*-

from debug import *

# Standard libraries import.
import subprocess

# Third libraries import.


# Projet modules import.


######################

class NCTM_Help():
    """
    Display the help (mainly man page) of a given binary.

    Public attributes.
        help_win = A pad window.
    """

    # Private attributes.
    # __maxy = maximum of lines.
    # __maxx = maximum of columns.
    # __binpath = the path of the binary.
    # __binhelp = the whatis of the binary.

    __KEY_q = [ord('q'), ord('Q')]

    # Public methods.
    def __init__(self, binpath, binhelp, maxy, maxx):
        """
        __init__ : initiate class
        @parameters : binpath = the full path of the binary.
                      binhelp = the whatis of the binary.
                      maxy = maximum of lines.
                      maxx = maximum of columns.
        @return : none.
        """
        self.help_win = curses.newpad(maxy, maxx)
        self.__maxy = maxy
        self.__maxx = maxx

        self.__binpath = binpath
        self.__binhelp = binhelp

        self.mainloop()

    def mainloop(self):
        """
        Main loop.
        @parameters : none.
        @return : none.
        """
        keypressed =""

        while keypressed not in self.__KEY_q:

            # NOTE: debug
#            printthis("self.__binpath", self.__binpath, self.help_win, 0, 0)
#            printthis("self.__binhelp", self.__binhelp, self.help_win, 5, 0)

            if not self.__binhelp:
                self.__no_manpage_display()
            else:
                self.__manpage_display()

            self.help_win.refresh(0, 0, 0, 0, self.__maxy, self.__maxx)
            curses.doupdate()

            keypressed = self.help_win.getch()


    # Private methods.
    def __no_manpage_display(self):
        """
        Display a message if no manpage found.
        @parameters : none.
        @return : none.
        """
        no_manpage = "No manpage found for this program !"
        len_no_manpage = len(no_manpage)
        no_manpage_midx = (self.__maxx >> 1) - (len_no_manpage >> 1) - len_no_manpage % 2
        self.help_win.addstr(self.__maxy >> 1,  no_manpage_midx, no_manpage)

    def __manpage_display(self):
        """
        Display a message if no manpage found.
        @parameters : none.
        @return : none.
        """
        manpage = subprocess.check_output(['man', self.__binpath],
                                          stderr=subprocess.STDOUT).decode('UTF-8')

        self.help_win.addstr(0, 0, manpage[:self.__maxx])

######################

if __name__ == "__main__":
    help(My_class)
