# -*- coding: utf-8 -*-

from debug import *

# Standard libraries import.
import curses.textpad as textpad
import subprocess

# Third libraries import.


# Projet modules import.


######################

class NCTM_Run():
    """
    Display man, if exists, at top part of view, an waiting for options at the bottom part.

    Public attributes.

    """

    # Private attributes.
    # __main_win = parent window.
    # __maxy = maximum of lines.
    # __maxx = maximum of columns.
    # __pmaxx = maximum of lines of the pan.
    # __pmaxy = maximum of columns of the pan.
    # __binpath = the path of the binary.
    # __binman = the whatis of the binary.
    # __first_line = first line to display in pad.
    # __manpage = dictinnary as {'content' : content of manpage,
    #                            'nblines' : number of lines ,
    #                            'nbcols' : number of columns (caracters)}

    __KEY_QUIT = 27

    # Public methods.
    def __init__(self, main_win, binpath, binman, maxy, maxx):
        """
        __init__ : initiate class
        @parameters : binpath = the full path of the binary.
                      binman = the whatis of the binary.
                      maxy = maximum of term (main win) lines.
                      maxx = maximum of term (main win) columns.
        @return : none.
        """
#        self.__binman = binman
        self.__binpath = binpath

        self.__main_win = main_win
        self.__maxx = maxx
        self.__maxy = maxy

        # Init self.__manpage{},
#        if not self.__binman:
#            self.__no_manpage_found()
#        else:
#            self.__manpage_found()
#
        # to init the followers.
        self.__pmaxy = 5
        self.__pmaxx = self.__maxx

        self.run_win = curses.newpad(self.__pmaxy, self.__pmaxx - 2)

#        self.__opt_win = textpad.rectangle(self.run_win, 0, 0, 1, 1)
        self.__opt_win = textpad.Textbox(self.run_win)
        self.__opt_win.stripspaces = True

        self.run_win.keypad(1)

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
            curses.KEY_PPAGE : self.__keyup_pressed
        }

        keypressed =""

        self.__first_line = 0

        while keypressed != self.__KEY_QUIT:
            if self.__main_win.is_wintouched:      # Window resizing detection curses.
                self.__update_run()

            if keypressed in callback.keys():
                callback[keypressed](keypressed)

            self.__runpage_display()

            keypressed = self.run_win.getch()

    # Private methods.
    def __keydown_pressed(self, key=None):
        """
        Called if down or page down key has been pressed.
        @parameters : key = which key has been pressed. None by default.
        @return : none.
        """
        if key == curses.KEY_NPAGE:
            step = self.__maxy - 2

        else:               # Normal arrow key.
            step = 1

        self.__first_line += step

        if self.__pmaxy - self.__first_line < self.__maxy:
            self.__first_line = self.__pmaxy - self.__maxy

    def __keyup_pressed(self, key=None):
        """
        Called if down or page down key has been pressed.
        @parameters : key = which key has been pressed. None by default.
        @return : none.
        """
        if key == curses.KEY_PPAGE:
            step = self.__maxy - 2

        else:       # Normal arrow key.
            step = 1

        self.__first_line -= step

        if self.__first_line < 0:
            self.__first_line = 0

    def __update_run(self):
        """
        Update to refresh main window.
        @parameters : none.
        @return : none.
        """
        self.__main_win.clear()
        self.run_win.clear()
        self.__maxy, self.__maxx = self.__main_win.getmaxyx()
        self.run_win.box()
        self.run_win.addstr(self.__pmaxy - 1, 1, "ESC : exit", curses.A_REVERSE)
        self.run_win.addstr(2, 1, "> ")
        self.run_win.addstr(0, 1, "Run : {} - UNDER BUILDING".format(self.__binpath), curses.A_REVERSE)

#        self.__fill_pad()

#    def __fill_pad(self):
#        """
#        Fill the pad with manpage.
#        @parameters : none.
#        @return : none.
#        """
#        self.run_win.addstr(0, 0, "azertyuio")

    def __runpage_display(self):
        """
        Fill the pad with manpage.
        @parameters : none.
        @return : none.
        """
        ymax,  xmax = self.run_win.getmaxyx()
        ymid = (self.__maxy >> 1) - (ymax >> 1)
        try:
            self.run_win.refresh(0, 0, ymid, 1, self.__maxy - 1, self.__maxx - 1)
            self.__opt_win.edit(er)
        except:
            pass

        curses.doupdate()

######################

if __name__ == "__main__":
    help(My_class)
