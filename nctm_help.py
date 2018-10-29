# -*- coding: utf-8 -*-

from debug import *

# Standard libraries import.
import curses.textpad
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
    # __main_win = parent window.
    # __maxy = maximum of lines.
    # __maxx = maximum of columns.
    # __pmaxx = maximum of lines of the pan.
    # __pmaxy = maximum of columns of the pan.
    # __binpath = the path of the binary.
    # __binhelp = the whatis of the binary.
    # __first_line = first line to display in pad.
    # __manpage = dictinnary as {'content' : content of manpage,
    #                            'nblines' : number of lines ,
    #                            'nbcols' : number of columns (caracters)}

    __KEY_QUIT = [ord('q'), ord('Q')]

    # Public methods.
    def __init__(self, main_win, binpath, binhelp, maxy, maxx):
        """
        __init__ : initiate class
        @parameters : binpath = the full path of the binary.
                      binhelp = the whatis of the binary.
                      maxy = maximum of term (main win) lines.
                      maxx = maximum of term (main win) columns.
        @return : none.
        """
        self.__binhelp = binhelp
        self.__binpath = binpath

        self.__main_win = main_win
        self.__maxx = maxx
        self.__maxy = maxy

        # Init self.__manpage{},
        if not self.__binhelp:
            self.__no_manpage_found()
        else:
            self.__manpage_found()

        # to init the followers.
        self.__pmaxy = self.__maxy if self.__manpage['nblines'] < self.__maxy else self.__manpage['nblines']
        self.__pmaxx = self.__manpage['nbcols']

        self.help_win = curses.newpad(self.__pmaxy, self.__pmaxx + 1)

        self.help_win.keypad(1)

        self.__fill_pad(not(self.__binhelp))

        self.help_win.box()

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

        while keypressed not in self.__KEY_QUIT:
            if self.__main_win.is_wintouched:      # Window resizing detection curses.
                self.__updatehelp()

            if keypressed in callback.keys():
                callback[keypressed](keypressed)

            self.__manpage_display(self.__first_line)

            keypressed = self.help_win.getch()

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

    def __updatehelp(self):
        """
        Update to refresh main window.
        @parameters : none.
        @return : none.
        """
        self.__main_win.clear()
        self.__maxy, self.__maxx = self.__main_win.getmaxyx()

    def __fill_pad(self, one_line):
        """
        Fill the pad with manpage.
        @parameters : none.
        @return : none.
        """
        if one_line:
            len_content = len(self.__manpage['content'][0])
            line = self.__maxy >> 1
            col = (self.__maxx >> 1) - (len_content >> 1) - len_content % 2

            self.help_win.addstr(line, col, self.__manpage['content'][0])

        else:
            line = 1

            for content in self.__manpage['content']:
                self.help_win.addstr(line, 1, content)
                line += 1

    def __manpage_display(self, from_line):
        """
        Fill the pad with manpage.
        @parameters : from_line = line from where to begin.
        @return : none.
        """
        try:
            self.help_win.refresh(from_line, 0, 0, 0, self.__maxy - 1, self.__maxx - 1)
        except:
            pass

        curses.doupdate()

######################

if __name__ == "__main__":
    help(My_class)
