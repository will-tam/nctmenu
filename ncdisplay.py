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
        mainwin = from curses stdscr. The main window.
        conf = the config class address.
    """

    # Private attributes.
    # __bins_to_show = list of config class found_bins dict keys.
    # __first_index = first element to display in __bins_to_show list.
    # __maxitem = length of __bins_to_show list.
    # __oldmaxy, __oldmaxx = size of window before resize it.

    __KEY_ESC = 27
    __KEY_ENTER = 10
    __KEY_h = ord('h')
    __KEY_H = ord('H')

    # Public methods.
    def __init__(self, stdscr, conf):
        """
        __init__ : initiate class
        @parameters : stdscr = represents the whole screen.
        @return : none.
        """
        self.mainwin= stdscr
        self.conf = conf

        self.__bins_to_show = [k for k in self.conf.found_bins.keys()]
        self.__first_index = 0
#        self.__first_index = 4320
        self.__maxitem = len(self.__bins_to_show)

        curses.resizeterm(50, 80)   # TODO: À effacer après MaP.
        self.__oldmaxy, self.__oldmaxx = (0, 0)

        self.run()

    def run(self):
        """
        main loop.
        @parameters : none.
        @return : none.
        """
        callback = {
            curses.KEY_DOWN : self.__keydown_pressed,
            curses.KEY_NPAGE : self.__keydown_pressed,
            curses.KEY_UP : self.__keyup_pressed,
            curses.KEY_PPAGE : self.__keyup_pressed,
            self.__KEY_ENTER : None,
            self.__KEY_h : None,
            self.__KEY_H : None,
        }

        keypressed =""

        curses.curs_set(0)  # No carret visible.

        while keypressed != self.__KEY_ESC:
            # Window responsive.
            self.__maxy, self.__maxx = self.mainwin.getmaxyx()

            if self.mainwin.is_wintouched:      # Window resizing detection curses.
                self.__refreshmain()

#            self.mainwin.move(3, 1) # Set carret in (x=1,y=3).

            # NOTE: debug
#            printthis("keypressed", "{}".format(keypressed), self.mainwin, 3, 1, )

            if keypressed in callback.keys():
                # NOTE: debug
#                printthis("Inside", "{0} - {1}".format(keypressed, callback[keypressed]), self.mainwin, 7, 1)
                callback[keypressed](keypressed)

            # TODO: à changer de place ou faire autrement.
            info = "{0}/{1}".format(self.__first_index, self.__maxitem)
            self.mainwin.addstr(0, 0, info, curses.A_BOLD)

            self.mainwin.refresh()
            curses.doupdate()
            keypressed = self.mainwin.getch()

    # Private methods.
    def __keydown_pressed(self, key=None):
        """
        Called if down or page down key pressed.
        @parameters : key = which key has been pressed. None by default.
        @return : none.
        """
        if key == curses.KEY_NPAGE:
            step = self.__maxy - 5  # -1 - 4
            if self.__first_index + step < self.__maxitem:
                self.__first_index += step
        else:
            if self.__first_index < self.__maxitem:
                self.__first_index += 1

    def __keyup_pressed(self, key=None):
        """
        Called if up or page up key pressed.
        @parameters : key = which key has been pressed. None by default.
        @return : none.
        """
        if key == curses.KEY_PPAGE:
            step = self.__maxy - 5  # -1 - 4
            if self.__first_index - step > -1:
                self.__first_index -= step
        else:
            if self.__first_index > 0:
                self.__first_index -= 1

    # TODO: Autres touches à partir d'ici.


    def __make_cells(self):
        """
        Draw the informations' cells.
        @parameters : none.
        @return : none.
        """
        # Headers to display
        programs = "Programs"
        whatis = "What  is"
        termonly = "Term  only"
        sep = "|"

        nbspace = (self.__maxx - 2) // 3    # The space beetween items.
        nbspacediv3 = (nbspace // 3)  # The space inside a cell : space somestuff space.

        # Header cells.
        header = nbspacediv3*" " + programs + nbspacediv3*" " + sep
        header += nbspacediv3*" " + whatis + nbspacediv3*" " + sep
        header += nbspacediv3*" " + termonly

        #TODO: Really need ?
        # ###########################
        # Empty cells.
        cell = ((nbspacediv3 << 1) + len(programs))*" " + sep
        cell += ((nbspacediv3 << 1) + len(programs))*" " + sep
        cell += ((nbspacediv3 << 1) + len(programs))*" "
        # ###########################

        self.mainwin.addstr(1, 1, header)

        self.mainwin.addstr(2, 1, (self.__maxx - 2)*"-")

        #TODO: Remove if cell = lines are removed.
        # ###########################
        for lin in range(3, self.__maxy):
            self.mainwin.addstr(lin, 1, cell)
        # ###########################

    def __updatedata(self):
        """
        Fill cells with datas according scrolling.
        @parameters : none.
        @return : none.
        """
        # NOTE: debug
#        printthis("Inside function", "{}".format(self.__updatedata.__name__), self.mainwin, 6, 1)

#        for k, v in self.conf.found_bins.items():
#            print(k, "  ", v[0], "  ", v[1])

        for lin in range(3, self.__maxy - 13):
            bin = self.__bins_to_show[self.__first_index + lin - 3]
            help = self.conf.found_bins[bin][0]
            term = self.conf.found_bins[bin][1]

            self.mainwin.addstr(lin, 1, "{0} {1}".format(lin - 3, bin))

    def __refreshmain(self):
        """
        Update to refresh main window.
        @parameters : none.
        @return : none.
        """
        self.mainwin.clear()
        self.mainwin.box()

        title = "{0} - {1}".format(PRGNAME, VERSION)[:self.__maxx]
        statusbar = "(P)UP/(P)DOWN arrows : navigate - H : more help - ENTER : run - ESC : exit"

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
