# -*- coding: utf-8 -*-

from .debug import *

# Standard libraries import.
import curses

# Third libraries import.


# Projet modules import.

from .infos import PRGNAME, VERSION
from . import config
from . import nctm_man
from . import nctm_help
from . import nctm_run
from . import sorted_according as sortacc

######################

class NCTM_Display():
    """
    Display menu with ncurse lib.

    Public attributes.
        main_win = from curses stdscr. The main window.
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
    # __ext = regex compilation to find extensions (see pattern).
    # __sorting_idx = index of the sorting functions in __sorting_func list.

    # Keys definition values.
    __KEY_QUIT = 27
    __KEY_ENTER = 10
    __KEY_h = ord('h')
    __KEY_H = ord('H')
    __KEY_m = ord('m')
    __KEY_M = ord('M')
    __KEY_p = ord('p')
    __KEY_P = ord('P')
    __KEY_s = ord('s')
    __KEY_S = ord('S')

    __sep = "|"     # Column separator.

    # Headers to display.
    __headers = {'programs' : "Programs - ",
                 'whatis' : "Wath is",
                 'termonly' : "Term only",
    }
    # And their length.
    __hlen = {'programs' : len(__headers['programs']),
              'whatis' : len(__headers['whatis']),
              'termonly' : len(__headers['termonly']),
    }

    # Sorting functions.
    __sorting_func = [sortacc.Sorted_according().paths,
                      sortacc.Sorted_according().filenames,
                      sortacc.Sorted_according().documentations_exist,
    ]
    __sorting_func_name = ["By path     ",
                           "By filename ",
                           "With man 1st",
    ]

    # Public methods.
    def __init__(self, stdscr, conf, rawlist=False):
        """
        __init__ : initiate class
        @parameters : stdscr = represents the whole screen.
                      conf = the config address.
                      rawlist = True if only display raw list.
        @return : none.
        """

        self.main_win= stdscr
        self.conf = conf

        self.__bins_to_show = [k for k in self.conf.found_bins.keys()]
        self.__bins_list_index = 0      # Sorting by paths by default.
        self.__first_display_bin_index = 0
        self.__underline_index = 0
        self.__maxitem = len(self.__bins_to_show)

        self.__oldmaxy, self.__oldmaxx = (0, 0)

        if rawlist:
            self.__sorting_idx = 0  # Sort by paths
            self.__rawlist()

        else:
            self.__sorting_idx = 1  # Sort by filenames

            self.__maxy, self.__maxx = self.main_win.getmaxyx()

            if curses.has_colors():
                curses.init_pair(1, curses.COLOR_RED, 0)
                curses.init_pair(2, curses.COLOR_CYAN, 0)
                curses.init_pair(3, curses.COLOR_YELLOW, 0)
    #           TODO: Effacer les paires de couleur inutiles.
    #            curses.init_pair(3, curses.COLOR_GREEN, 0)
    #            curses.init_pair(4, curses.COLOR_MAGENTA, 0)
    #            curses.init_pair(5, curses.COLOR_BLUE, 0)
    #            curses.init_pair(6, curses.COLOR_CYAN, 0)
    #            curses.init_pair(7, curses.COLOR_WHITE, 0)

    #        self.conf.found_bins = self.__sorting_func[self.__sorting_idx](self.conf.found_bins)
            self.__keyS_pressed()

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
            self.__KEY_m : self.__keyM_pressed,
            self.__KEY_M : self.__keyM_pressed,
            self.__KEY_p : self.__keyP_pressed,
            self.__KEY_P : self.__keyP_pressed,
            self.__KEY_s : self.__keyS_pressed,
            self.__KEY_S : self.__keyS_pressed,
        }

        keypressed =""

        curses.curs_set(0)  # No carret visible.

        while keypressed != self.__KEY_QUIT:
            # Window responsive.
            if self.main_win.is_wintouched:      # Window resizing detection curses.
                self.__updatemain()

            if keypressed in callback.keys():
                callback[keypressed](keypressed)
                self.__updatedata()

            self.main_win.refresh()
            curses.doupdate()

            keypressed = self.main_win.getch()

    # Private methods.
    def __rawlist(self):
        """
        Display in raw list to be redirected in file, for example.
        @parameters = none.
        @return = none.
        """
        self.conf.found_bins = self.__sorting_func[self.__sorting_idx](self.conf.found_bins)
        print("\nFull/path/of/bin--whatis--term only(term)|graphic(x)\n")

        for found_bin in self.conf.found_bins:
            help = self.conf.found_bins[found_bin][0]
            term = self.conf.found_bins[found_bin][1]

            print("{}--{}--{}".format(found_bin, help, term))

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
        nctm_help.NCTM_Help(self.main_win, self.__maxy, self.__maxx)

        self.__updatemain()     # Init again if any changes while help window displaying.

    def __keyM_pressed(self, key=None):
        """
        Called if key 'm' or 'M' has been pressed.
        @parameters : key = which key has been pressed. None by default.
        @return : none.
        """
        full_path = self.__bins_to_show[self.__first_display_bin_index + self.__underline_index]
        man = self.conf.found_bins[full_path][0]
        manpage_win = nctm_man.NCTM_Man(self.main_win, full_path, man, self.__maxy, self.__maxx)
        manpage_win.mainloop()

        self.__updatemain()     # Init again if any changes while help window displaying.

    def __keyP_pressed(self, key=None):
        """
        Called if key 'p' or 'P' has been pressed.
        @parameters : key = which key has been pressed. None by default.
        @return : none.
        """
        if curses.has_colors():
            self.main_win.attrset(curses.color_pair(2) | curses.A_BOLD | curses.A_REVERSE)
        else:
            self.main_win.attrset(curses.A_BOLD | curses.A_REVERSE)

        full_path = self.__bins_to_show[self.__first_display_bin_index + self.__underline_index]

        # Keep only the string before the last "/" and print it.
        self.main_win.addstr(1, self.__hlen['programs'] + 1, full_path[:full_path.rfind('/')])

        self.main_win.attrset(0)

    def __keyS_pressed(self, key=None):
        """
        Called if key 's' or 'S' has been pressed.
        @parameters : key = which key has been pressed. None by default.
        @return : none.
        """
        self.__sorting_idx = (self.__sorting_idx + 1) % 3   # Possibility in only 3 kinds of search.

        self.conf.found_bins = self.__sorting_func[self.__sorting_idx](self.conf.found_bins)

        if curses.has_colors():
            self.main_win.attrset(curses.color_pair(2) | curses.A_BOLD)
        else:
            self.main_win.attrset(curses.A_BOLD)

        self.__bins_to_show = [k for k in self.conf.found_bins.keys()]

        self.main_win.addstr(1, self.__hlen['programs'] + 1, self.__sorting_func_name[self.__sorting_idx])

        self.main_win.attrset(0)

    def __keyENTER_pressed(self, key=None):
        """
        Called if enter key has been pressed.
        @parameters : key = which key has been pressed. None by default.
        @return : none.
        """
        full_path = self.__bins_to_show[self.__first_display_bin_index + self.__underline_index]
        man = self.conf.found_bins[full_path][0]
        nctm_run.NCTM_Run(self.main_win, full_path, man, self.__maxy, self.__maxx)

        self.__updatemain()     # Init again if any changes while help window displaying.

    def __make_cells_headers(self):
        """
        Draw the informations' cells.
        @parameters : none.
        @return : none.
        """
        all_space_left = self.__maxx - self.__hlen['termonly'] - 3 # -2 (border) -1 separator.
        self.__space_left = all_space_left * 40 // 100
        self.__space_right = all_space_left * 60 // 100

        header = self.__headers['programs'] + (self.__space_left - self.__hlen['programs'])*" "
        header += self.__sep + self.__headers['whatis'] + (self.__space_right - self.__hlen['whatis'] - 1)*" "
        header += self.__sep + self.__headers['termonly']

        self.main_win.addstr(1, 1, header)

        self.main_win.addstr(2, 1, (self.__maxx - 2)*"-")

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

                infos = full_path.split('/').pop()     # Could be on only one line, but
                infos = infos[:self.__space_left - 2]  # doesn't clear code.

                infos += (self.__space_left - len(infos))*" " + self.__sep
                infos += help
                infos += (self.__space_right - len(help) - 1)*" " + self.__sep
                infos += "Y" if term == "term" else "N"
                infos += (self.__maxx  - len(infos) - 2)*" "
            else:
                infos = (self.__maxx - 2)*" "

            if self.__fakeBin(full_path):
                if curses.has_colors():
                    self.main_win.attrset(curses.color_pair(1))
                else:
                    self.main_win.attrset(curses.A_BOLD | curses.A_REVERSE | curses.A_BLINK)

            self.main_win.addstr(lin, 1, infos)
            self.main_win.attrset(0)

            line_to_show = (self.__underline_index + 3)
            self.main_win.chgat(line_to_show, 1, self.__maxx - 2, curses.A_REVERSE)

            info = " {0}/{1} - h / H : Help".format(self.__bins_list_index + 1, self.__maxitem)

            self.main_win.addstr(self.__maxy - 1, 0, info, curses.A_BOLD)

    def __updatemain(self):
        """
        Update to refresh main window.
        @parameters : none.
        @return : none.
        """
        self.main_win.clear()

        self.__maxy, self.__maxx = self.main_win.getmaxyx()

        self.main_win.box()

        title = "{0} - {1}".format(PRGNAME, VERSION)[:self.__maxx]
#        statusbar = "(P)UP/(P)DOWN arrows : navigate - M : manpage - P : path - S : sort - ENTER : run - ESC : exit"

        len_title = len(title)
#        len_sb = len(statusbar)

        title_middlex = (self.__maxx >> 1) - (len_title >> 1) - len_title % 2
#        sb_middlex = (self.__maxx >> 1) - (len_sb >> 1) - len_sb % 2

        # TODO: Calcul ou trouver astuce pour éviter le crash en cas de dépacement du nb de car sur fenêtre trop petite
        # en lieu et place du try ci-dessous.
#        title = title[:self.__maxx]
#        statusbar = statusbar[:self.__maxx - sb_middlex]

        try:
            self.main_win.addstr(0, title_middlex, title)
#            self.main_win.addstr(self.__maxy - 1, sb_middlex, statusbar, curses.A_REVERSE)
        except:
            if curses.has_colors():
                self.main_win.attrset(curses.color_pair(3) | curses.A_REVERSE | curses.A_BOLD)
            else:
                self.main_win.attrset(curses.A_BOLD | curses.A_REVERSE | curses.A_BLINK)

            self.main_win.addstr(self.__maxy - 1, 1, "80X50 at least")
            self.main_win.attrset(0)

        self.__make_cells_headers()

        """
        """

        if curses.has_colors():
            self.main_win.attrset(curses.color_pair(2) | curses.A_BOLD)
        else:
            self.main_win.attrset(curses.A_BOLD)

        self.main_win.addstr(1, self.__hlen['programs'] + 1, self.__sorting_func_name[self.__sorting_idx])

        self.main_win.attrset(0)

        """
        """

        self.__updatedata()

        self.__oldmaxy, self.__oldmaxx = (self.__maxy, self.__maxx)

    def __fakeBin(self, full_path):
        """
        Detect if the file shouldn't be a binary file.
        Typically a library, picture, ... file with executable UNIX ACL tag.
        @parameters : full_path = the absolute path of binary.
        @return : True if the file shouldn't be a binary (see FORBID_EXT in config module)
        """
        pieces_of_path = [e for e in full_path.split("/") if e] # Remove the "" element.
        file = pieces_of_path.pop()     # Extract only file name.
        ext = file.rsplit('.').pop()    # Extract extension.

        if ext.lower() in config.FORBID_EXT:
            return True

        return False

######################

if __name__ == "__main__":
    help(NCDisplay)
