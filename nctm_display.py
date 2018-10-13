# -*- coding: utf-8 -*-

from debug import *

# Standard libraries import.
import curses

# Third libraries import.


# Projet modules import.
from infos import PRGNAME, VERSION
import config
import nctm_help

######################

class NCTM_Display():
    """
    Display menu with ncurse lib.

    Public attributes.
        mainwin = from curses stdscr. The main window.
        conf = the config class address.
    """

    # Private attributes.
    # __bins_to_show = list of config class found_bins dict keys.
    # __bins_list_index = index of element to display from __bins_to_show list.
    # __first_display_bin_index = index of the first binarie in list.
    # __underline_index = line to underline.
    # __maxitem = length of __bins_to_show list.
    # __maxx = number max of col.
    # __maxy = number max of line.
    # __space_left = percentage of space to write bins' name.
    # __space_right = percentage of space to write bin's help prevue.
    # __oldmaxy, __oldmaxx = size of window before resize it.

    __KEY_ESC = 27
    __KEY_ENTER = 10
    __KEY_h = ord('h')
    __KEY_H = ord('H')

    __sep = "|"

    # Public methods.
    def __init__(self, stdscr, conf):
        """
        __init__ : initiate class
        @parameters : stdscr = represents the whole screen.
                      conf = the config address.
        @return : none.
        """
        self.mainwin= stdscr
        self.conf = conf

        self.__bins_to_show = [k for k in self.conf.found_bins.keys()]
        self.__bins_list_index = 0
        self.__first_display_bin_index = 0
        self.__underline_index = 0
        self.__maxitem = len(self.__bins_to_show)

        self.__oldmaxy, self.__oldmaxx = (0, 0)

        self.__maxy, self.__maxx = self.mainwin.getmaxyx()

        curses.resizeterm(self.__maxy, 80)   # TODO: À effacer après MaP. On ne force que la largeur du term.

        self.mainloop()

    def mainloop(self):
        """
        Main loop.
        @parameters : none.
        @return : none.
        """
        callback = {
            curses.KEY_DOWN : self.__keydown_pressed,
            curses.KEY_NPAGE : self.__keydown_pressed,
            curses.KEY_UP : self.__keyup_pressed,
            curses.KEY_PPAGE : self.__keyup_pressed,
            self.__KEY_ENTER : self.__keyENTER_pressed,
            self.__KEY_h : self.__keyH_pressed,
            self.__KEY_H : self.__keyH_pressed,
        }

        keypressed =""

        curses.curs_set(0)  # No carret visible.

        while keypressed != self.__KEY_ESC:
            # Window responsive.
            if self.mainwin.is_wintouched:      # Window resizing detection curses.
                self.__updatemain()

            # NOTE: debug
#            printthis("keypressed", "{}".format(keypressed), self.mainwin, 3, 1, )

            if keypressed in callback.keys():
                # NOTE: debug
#                printthis("Inside", "{0} - {1}".format(keypressed, callback[keypressed]), self.mainwin, 7, 1)
                callback[keypressed](keypressed)
                self.__updatedata()

            # TODO: à changer de place ou faire autrement.
            info = "{0}/{1}".format(self.__bins_list_index + 1, self.__maxitem)
            self.mainwin.addstr(0, 0, info, curses.A_BOLD)

            self.mainwin.refresh()
            curses.doupdate()

            keypressed = self.mainwin.getch()

    # Private methods.
    def __keydown_pressed(self, key=None):
        """
        Called if down or page down key has been pressed.
        @parameters : key = which key has been pressed. None by default.
        @return : none.
        """
        old_underline_index = self.__underline_index

        if key == curses.KEY_NPAGE:
            step = self.__maxy - 5  # -4 (Head) -1 (Foot).

        else:       # Normal arrow key.
            step = 1

        # Check the last item is reached.
        if self.__bins_list_index + step > self.__maxitem - 1:
            step = self.__maxitem - self.__bins_list_index - 1      # Adjust the step.

        self.__bins_list_index += step
        self.__underline_index += step

        # Bottom is reached.
        if self.__underline_index > self.__maxy - 5:    # -4 (Head) -1 (Foot).
            self.__underline_index = old_underline_index
            self.__first_display_bin_index += step

    def __keyup_pressed(self, key=None):
        """
        Called if up or page up key has been pressed.
        @parameters : key = which key has been pressed. None by default.
        @return : none.
        """
        old_underline_index = self.__underline_index

        if key == curses.KEY_PPAGE:
            step = self.__maxy - 5  # -4 (Head) -1 (Foot).

        else:       # Normal arrow key.
            step = 1

        # Check the first item is reached.
        if self.__bins_list_index - step < 0:
            step = 0

        self.__bins_list_index -= step
        self.__underline_index -= step

        # Top is reached.
        if self.__underline_index < 0:
            self.__underline_index = old_underline_index
            self.__first_display_bin_index -= step

    def __keyH_pressed(self, key=None):
        """
        Called if key 'h' or 'H' has been pressed.
        @parameters : key = which key has been pressed. None by default.
        @return : none.
        """
        full_path = self.__bins_to_show[self.__first_display_bin_index + self.__underline_index]
        help = self.conf.found_bins[full_path][0]
        nctm_help.NCTM_Help(full_path, help, self.__maxy, self.__maxx)

    def __keyENTER_pressed(self, key=None):
        """
        Called if enter key has been pressed.
        @parameters : key = which key has been pressed. None by default.
        @return : none.
        """
        pass

    def __make_cells_headers(self):
        """
        Draw the informations' cells.
        @parameters : none.
        @return : none.
        """
        # Headers to display
        programs = "Programs"
        whatis = "What is"
        termonly = "Term only"

        len_programs = len(programs)
        len_whatis = len(whatis)
        len_termonly = len(termonly)

        all_space_left = self.__maxx - len_termonly - 3 # -2 (border) -1 separator.
        self.__space_left = all_space_left * 40 // 100
        self.__space_right = all_space_left * 60 // 100

        header = programs + (self.__space_left - len_programs)*" "
        header += self.__sep + whatis + (self.__space_right - len_whatis - 1)*" "
        header += self.__sep + termonly

        self.mainwin.addstr(1, 1, header)

        self.mainwin.addstr(2, 1, (self.__maxx - 2)*"-")

    def __updatedata(self):
        """
        Fill cells with datas according scrolling.
        @parameters : none.
        @return : none.
        """
        for lin in range(3, self.__maxy - 1):

            if self.__first_display_bin_index + lin - 3 < self.__maxitem:

                full_path = self.__bins_to_show[self.__first_display_bin_index + lin - 3]
                help = self.conf.found_bins[full_path][0][:self.__space_right - 2]
                term = self.conf.found_bins[full_path][1]

                bin_name = full_path[:self.__space_left - 2]

                infos = "{0}".format(bin_name.split('/').pop())
                infos += (self.__space_left - len(infos))*" " + self.__sep
                infos += "{}".format(help)
                infos += (self.__space_right - len(help) - 1)*" " + self.__sep
                infos += "Y" if term == "term" else "N"
                infos += (self.__maxx  - len(infos) - 2)*" "

            else:
                infos = (self.__maxx - 2)*" "

            self.mainwin.addstr(lin, 1, infos)

            line_to_show = (self.__underline_index + 3)
            self.mainwin.chgat(line_to_show, 1, self.__maxx - 2, curses.A_REVERSE)

    def __updatemain(self):
        """
        Update to refresh main window.
        @parameters : none.
        @return : none.
        """
        self.mainwin.clear()

        self.__maxy, self.__maxx = self.mainwin.getmaxyx()

        self.mainwin.box()

        title = "{0} - {1}".format(PRGNAME, VERSION)[:self.__maxx]
        statusbar = "(P)UP/(P)DOWN arrows : navigate - H : more help - ENTER : run - ESC : exit"

        len_title = len(title)
        len_sb = len(statusbar)

        title_middlex = (self.__maxx >> 1) - (len_title >> 1) - len_title % 2
        sb_middlex = (self.__maxx >> 1) - (len_sb >> 1) - len_sb % 2

        # TODO: Calcul ou trouver astuce pour éviter le crash en cas de dépacement du nb de car sur fenêtre trop petite
        # en lieu et place du try ci-dessous.
#        title = title[:self.__maxx]
#        statusbar = statusbar[:self.__maxx - sb_middlex]

        try:
            self.mainwin.addstr(0, title_middlex, title)
            self.mainwin.addstr(self.__maxy - 1, sb_middlex, statusbar)
        except:
            self.mainwin.addstr(self.__maxy - 1, 1, "80X50 at least")

        self.__make_cells_headers()
        self.__updatedata()

        self.__oldmaxy, self.__oldmaxx = (self.__maxy, self.__maxx)

######################

if __name__ == "__main__":
    help(NCDisplay)
