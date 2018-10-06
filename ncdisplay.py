# -*- coding: utf-8 -*-

from debug import *

# Standard libraries import.
import curses

# Third libraries import.


# Projet modules import.
from infos import PRGNAME, VERSION
import config

######################

class NCDisplay():
    """
    Display with ncurse lib.

    Public attributes.
    """

    # Private attributes.
    __KEY_ESC = 27

    # Public methods.
    def __init__(self, stdscr, conf):
        """
        __init__ : initiate class
        @parameters : stdscr = represents the whole screen.
        @return : none.
        """
        self.mainwin= stdscr
        self.conf = conf

        self.__bins_to_show = [k for k in self.conf.found_bins.keys()]  # TODO: Need to create the OrderedDict before.

        curses.resizeterm(50, 80)   # TODO: À effacer après MaP.
        self.__oldmaxy, self.__oldmaxx = (0, 0)

        self.run()

    def run(self):
        """
        main loop.
        @parameters : none.
        @return : none.
        """
        keypressed =""

        curses.curs_set(0)  # No carret visible.

        while keypressed != self.__KEY_ESC:
            # Window responsive.
            self.__maxy, self.__maxx = self.mainwin.getmaxyx()

            if self.__maxy != self.__oldmaxy or self.__oldmaxy != self.__maxx:
                self.__updateall()

            self.mainwin.move(3, 1) # Set carret in (x=1,y=3).

            self.mainwin.refresh()
            curses.doupdate()
            keypressed = self.mainwin.getch()

    # Private methods.
    def __make_cells(self):
        """
        Draw the informations' cells.
        @parameters : none.
        @return : none.
        """
        # Headers to display
        program = "Program"
        whatis = "What is"
        termonly = "Term only"
        sep = "|"

        nbspace = (self.__maxx - 2) // 3    # The space beetween items.
        nbspacediv3 = ((nbspace // 3) + 1)  # The space inside a cell : space somestuff space.

        # Header cells.
        header = nbspacediv3*" " + program + nbspacediv3*" " + sep
        header += nbspacediv3*" " + whatis + nbspacediv3*" " + sep
        header += nbspacediv3*" " + termonly

        # Empty cells.
        cell = ((nbspacediv3 << 1) + len(program))*" " + sep
        cell += ((nbspacediv3 << 1) + len(program))*" " + sep
        cell += ((nbspacediv3 << 1) + len(program))*" "

        self.mainwin.addstr(1, 1, header)

        for lin in range(2, self.__maxy):
            self.mainwin.addstr(lin, 1, cell)

    def __updatedata(self):
        """
        Fill cells with datas according scrolling.
        @parameters : none.
        @return : none.
        """
        pass
#        for k, v in self.conf.found_bins.items():
#            print(k, "  ", v[0], "  ", v[1])


    def __updateall(self):
        """
        Update to refresh main window.
        @parameters : none.
        @return : none.
        """
        self.mainwin.clear()
        self.mainwin.box()

        title = "{0} - {1}".format(PRGNAME, VERSION)[:self.__maxx]
        statusbar = "UP / DOWN arrows : navigate - h : more help - ENTER : run - ESC : exit"

        len_title = len(title)
        len_sb = len(statusbar)

        title_middlex = (self.__maxx >> 1) - (len_title >> 1) - len_title % 2
        sb_middlex = (self.__maxx >> 1) - (len_sb >> 1) - len_sb % 2
        self.__maxy -= 1

        # TODO: Calcul ou trouver astuce pour éviter le crash en cas de dépacement du nb de car sur fenêtre trop petite
        # en lieu et place du try ci-dessous.
#        title = title[:self.__maxx]
#        statusbar = statusbar[:self.__maxx - sb_middlex]

        try:
            self.mainwin.addstr(0, title_middlex, title)
            self.mainwin.addstr(self.__maxy, sb_middlex, statusbar)
        except:
            self.mainwin.addstr(self.__maxy - 1, 1, "80X50 at least")

        self.__make_cells()
        self.__updatedata()

        self.__oldmaxy, self.__oldmaxx = (self.__maxy, self.__maxx)

######################

if __name__ == "__main__":
    help(NCDisplay)
