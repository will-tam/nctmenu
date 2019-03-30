# -*- coding: utf-8 -*-

from debug import *

# Standard libraries import.
import curses.textpad

# Third libraries import.


# Projet modules import.


######################

class NCTM_Help():
    """
    Display help.

    Public attributes.
        help_win = A pad window.
    """

    # Private attributes.
    # __main_win = parent window.
    # __maxy = maximum of lines.
    # __maxx = maximum of columns.

    __KEY_QUIT = 27

    __HELP = ["ESC : exit the watching screen. In main one, exit program.",
              "ENTER : run the program highlighting.",
              "up / page up : one line / page up.",
              "down / page down : one /page down.",
              "m / M : program highlighting man page screen",
              "s / S : - sort by paths (default)",
              "        - file names (alpha sort)",
              "        - documented programs first",
              "p / P : show program highlighting path.",
              "h / H : this screen.",
    ]

    # Public methods.
    def __init__(self, main_win, maxy, maxx):
        """
        __init__ : initiate class
        @parameters : maxy = maximum of term (main win) lines.
                      maxx = maximum of term (main win) columns.
        @return : none.
        """
        self.__main_win = main_win
        self.__maxx = maxx
        self.__maxy = maxy

        self.help_win = curses.newpad(self.__maxy, self.__maxx + 1)

        self.help_win.keypad(1)

        self.mainloop()

    def mainloop(self):
        """
        Main loop.
        @parameters : none.
        @return : none.
        """
        keypressed =""

        while keypressed != self.__KEY_QUIT:
            if self.__main_win.is_wintouched:      # Window resizing detection curses.
                self.__updatehelp()

            self.__help_display()

            keypressed = self.help_win.getch()

    # Private methods.
    def __updatehelp(self):
        """
        Update to refresh main window.
        @parameters : none.
        @return : none.
        """
        self.__main_win.clear()
        self.help_win.clear()
        self.__maxy, self.__maxx = self.__main_win.getmaxyx()
        self.help_win.box()
        self.help_win.addstr(0, 1, "ESC : exit", curses.A_REVERSE)
        self.__fill_pad()

    def __fill_pad(self):
        """
        Fill the pad with manpage.
        @parameters : none.
        @return : none.
        """
        line = 2

        for content in self.__HELP:
            self.help_win.addstr(line, 1, content)
            line += 1

    def __help_display(self):
        """
        Fill the pad with help.
        @parameters : none.
        @return : none.
        """
        try:
            self.help_win.refresh(0, 0, 0, 0, self.__maxy - 1, self.__maxx - 1)
        except:
            pass

        curses.doupdate()

######################

if __name__ == "__main__":
    help(My_class)
