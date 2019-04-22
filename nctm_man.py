# -*- coding: utf-8 -*-

from debug import *

# Standard libraries import.
import curses.textpad
import subprocess

# Third libraries import.


# Projet modules import.


######################

class NCTM_Man():
    """
    Display the man page of a given binary.

    Public attributes.
        man_win = A pad window.
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
                      binman = the manpage of the binary.
                      maxy = maximum of term (main win) lines.
                      maxx = maximum of term (main win) columns.
                      only_man = True => man is only used for ... man ; False => somthing else uses manpage.
        @return : none.
        """
        self.__binman = binman
        self.__binpath = binpath

        self.__main_win = main_win
        self.__maxx = maxx
        self.__maxy = maxy

        self.__first_line = 0

        # Init self.__manpage{},
        if not self.__binman:
            self.__no_manpage_found()
        else:
            self.__manpage_found()

        # to init the followers.
        self.__pmaxy = self.__maxy if self.__manpage['nblines'] < self.__maxy else self.__manpage['nblines']
        self.__pmaxx = self.__manpage['nbcols']

        self.man_win = curses.newpad(self.__pmaxy, self.__pmaxx + 1)

        self.man_win.keypad(1)

    def mainloop(self):
        """
        Main loop.
        @parameters : none.
        @return : none.
        """
        callback = {
            curses.KEY_DOWN : self._keydown_pressed,
            curses.KEY_NPAGE : self._keydown_pressed,
            curses.KEY_UP : self._keyup_pressed,
            curses.KEY_PPAGE : self._keyup_pressed
        }

        keypressed =""

        while keypressed != self.__KEY_QUIT:
            if self.__main_win.is_wintouched:      # Window resizing detection curses.
                self._updateman()

            if keypressed in callback.keys():
                callback[keypressed](keypressed)

            self._manpage_display()

            keypressed = self.man_win.getch()

    # "Protected" methods.
    def _keydown_pressed(self, key=None):
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

    def _keyup_pressed(self, key=None):
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

    def _updateman(self, yadjustement=0):
        """
        Update to refresh main window.
        @parameters : yadjustement = number of line to remove in y.
        @return : none.
        """
        self.__maxy, self.__maxx = self.__main_win.getmaxyx()
        self.__main_win.clear()
        self.man_win.clear()
        self.__maxy -= yadjustement
        self.man_win.box()
        self.man_win.addstr(0, 1, "ESC : exit - yadjustement", curses.A_REVERSE)
        self.__fill_pad(not(self.__binman))

#    def _manpage_display(self, from_line=self.__first_line):
    def _manpage_display(self):
        """
        Display manpage from a line number.
        @parameters : from_line = line from where to begin.
        @return : none.
        """
        try:
#            self.man_win.refresh(from_line, 0, 0, 0, self.__maxy - 1, self.__maxx - 1)
            self.man_win.refresh(self.__first_line, 0, 0, 0, self.__maxy - 1, self.__maxx - 1)
        except:
            pass

        curses.doupdate()

    # Private methods.
    def __no_manpage_found(self):
        """
        Even if no manpage found, something to display.
        @parameters : none.
        @return : none.
        """
        content = "No manpage found for this program !"
        self.__manpage = {'content' : [content],
                          'nblines' : 1,
                          'nbcols' : self.__maxx}

    def __manpage_found(self):
        """
        If manpage found.
        @parameters : none.
        @return : none.
        """
        content = subprocess.check_output(['man', self.__binpath],
                                          stderr=subprocess.STDOUT).decode('UTF-8')

        content = content.splitlines()

        # This follow because some of them wants to use you, some of them wants to be used by you ... no
        # This follow because some manpage begins with '\n' caracters ! F**K !
        content_tmp = list(content) # To create an other real variable, not a reference to.

        for c in content:
            if c == '':
                content_tmp.pop(0)
            else:
                break

        content = content_tmp

        self.__manpage = {'content' : content,
                          'nblines' : len(content) + 1,    # Number of lines in list is the length of manpage.
                          'nbcols' : len(content[0]) + 3}  # First line of manpage give the width.

    def __fill_pad(self, one_line):
        """
        Fill the pad with manpage.
        @parameters : one_line = man page with only one line.
        @return : none.
        """
        if one_line:
            len_content = len(self.__manpage['content'][0])
            line = self.__maxy >> 1
            col = (self.__maxx >> 1) - (len_content >> 1) - len_content % 2

            self.man_win.addstr(line, col, self.__manpage['content'][0])

        else:
            line = 1

            for content in self.__manpage['content']:
                self.man_win.addstr(line, 1, content)
                line += 1

######################

if __name__ == "__main__":
    help(NCTM_Man)
