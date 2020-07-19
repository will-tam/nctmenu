# -*- coding: utf-8 -*-

from .debug import *

# Standard libraries import.
#import curses.textpad as ctextpad
import curses
import curses.ascii as cascii
import subprocess

# Third libraries import.


# Projet modules import.
from . import nctm_man


######################

class NCTM_Run(nctm_man.NCTM_Man):
    """
    NCTM_Man() class daughter.

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
    # __posy = y position in option edit.
    # __posx = x position in option edit.
    # __posx_limit_left = can't be gone lefter than this position.
    # __posx_limit_right = can't be gone righter than this position.
    # __cde_arg = arguments of the command.
    # __cde_arg_len = length of arguments of the command.
    # __curs_arg_pos = position in command arguments.

    __KEY_QUIT = 27
    __KEY_ENTER = 10

    __RUN_WIN_H = 5
    __PROMPT = "args > "

    # Public methods.
    def __init__(self, main_win, binpath, binman, maxy, maxx):
        """
        __init__ : initiate class
        @parameters : binpath = the full path of the binary.
                      binman = the manpage of the binary.
                      maxy = maximum of term (main win) lines.
                      maxx = maximum of term (main win) columns.
        @return : none.
        """
        self.__binman = binman
        self.__binpath = binpath

        self.__main_win = main_win
        self.__maxx = maxx
        self.__maxy = maxy

        # to init the followers.
        self.__pmaxy = self.__RUN_WIN_H
        self.__pmaxx = self.__maxx

        super().__init__(self.__main_win, self.__binpath, self.__binman, self.__maxy - self.__RUN_WIN_H, self.__maxx)

        self.run_win = curses.newpad(self.__pmaxy, self.__pmaxx - 2)

#        self.__opt_win = textpad.rectangle(self.run_win, 0, 0, 1, 1)
#        self.__opt_win = ctextpad.Textbox(self.run_win, insert_mode=True)

        self.__posy = 2
        self.__posx = len(self.__PROMPT) + 1
        self.__posx_limit_left = self.__posx
        self.__posx_limit_right = self.__posx

        self.__cde_arg = ""
        self.__cde_arg_len = 0
        self.__curs_arg_pos = 0

        self.run_win.keypad(1)
        #self.run_win.leaveok(0)

        curses.curs_set(2)
        self.mainloop()

    def mainloop(self):
        """
        Main loop.
        @parameters : none.
        @return : none.
        """
        callbacks = {
            curses.KEY_DOWN : super()._keydown_pressed,
            curses.KEY_NPAGE : super()._keydown_pressed,
            curses.KEY_UP : super()._keyup_pressed,
            curses.KEY_PPAGE : super()._keyup_pressed
        }

        keypressed =""

#        self.__first_line = 0

#        super().mainloop()

        while keypressed != self.__KEY_QUIT:
            if self.__main_win.is_wintouched:      # Window resizing detection curses.
                super()._updateman(self.__RUN_WIN_H)
                self.__updaterun()

            if keypressed:
                if keypressed in callbacks.keys():
                    callbacks[keypressed](keypressed)
                else:
                    self.__edit_args(keypressed)

            super()._manpage_display()
            self.__runpage_display()

            keypressed = self.run_win.getch()

        curses.curs_set(0)

    # Private methods.
    def __edit_args(self, ch):
        """
        Edit the arguments.
        @parameters : ch = the pressed key.
        @return : none.
        """
        callbacks = {
            curses.KEY_LEFT : self.__move_left,
            curses.KEY_RIGHT : self.__move_right,
            curses.KEY_HOME : self.__move_to_0,
            curses.KEY_END : self.__move_to_end,
            curses.KEY_DC : self.__del_right,
            curses.KEY_BACKSPACE : self.__del_left,
        }

        if cascii.isprint(ch):
            self.__add_ch(self.__curs_arg_pos, ch)
        elif ch in callbacks:
#            self.__cde_arg = str(callbacks[ch])
            callbacks[ch]()

        elif ch == self.__KEY_ENTER:
            self.__run_it(None, None)


        self.__updaterun()
        # TODO: À effacer après MaP.
#        self.run_win.addstr(self.__posy - 1, self.__posx, "{}".format(ch))

    def __add_ch(self, pos, ch):
        """
        Add a character at a position.
        @parameters : pos = position where add the character.
                      ch = character to add.
        @return : none
        """
        self.__cde_arg += chr(ch)
        self.__cde_arg_len = len(self.__cde_arg)
        self.__curs_arg_pos += 1
        self.__posx_limit_right += 1

    def __move_left(self):
        """
        Move curseur to left in args line.
        @parameters : none.
        @return : none.
        """
        if self.__curs_arg_pos > 0:
            self.__curs_arg_pos -= 1

    def __move_right(self):
        """
        Move curseur to right in args line.
        @parameters : none.
        @return : none.
        """
#        if self.__curs_arg_pos < self.__maxx - self.__posx_limit_left - 5:
        if self.__curs_arg_pos < self.__posx_limit_right - self.__posx_limit_left:
            self.__curs_arg_pos += 1

    def __move_to_0(self):
        """
        Delete a character at right of cursor position.
        @parameters : none.
        @return : none.
        """
        self.__curs_arg_pos = 0

    def __move_to_end(self):
        """
        Delete a character at right of cursor position.
        @parameters : none.
        @return : none.
        """
        self.__curs_arg_pos = self.__posx_limit_right - self.__posx_limit_left

    def __del_left(self):
        """
        Delete a character at left of cursor position.
        @parameters : none.
        @return : none.
        """
        pass

    def __del_right(self):
        """
        Delete a character at right of cursor position.
        @parameters : none.
        @return : none.
        """
        pass

    def __run_it(self, cde, args):
        """
        Delete a character at left of cursor position.
        @parameters : cde = commande to run.
                      args = arguments of this command.
        @return : return code of the command.
        """
        pass

    def __updaterun(self):
        """
        Update to refresh main window.
        @parameters : none.
        @return : none.
        """
        self.__main_win.erase() # No flashing screen.
        self.run_win.erase()    # No flashing screen.
        self.__maxy, self.__maxx = self.__main_win.getmaxyx()
        self.run_win.box()
        self.run_win.addstr(self.__pmaxy - 1, 1, "ESC : exit", curses.A_REVERSE)
        self.run_win.addstr(2, 1, self.__PROMPT + self.__cde_arg)
        self.run_win.addstr(0, 1, "Run : {} - UNDER BUILDING".format(self.__binpath), curses.A_REVERSE)

        self.run_win.move(self.__posy, self.__posx + self.__curs_arg_pos)

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
#        ymax,  xmax = self.run_win.getmaxyx()
#        ymid = (self.__maxy >> 1) - (ymax >> 1)
        try:
            self.run_win.refresh(0, 0, self.__maxy - self.__RUN_WIN_H, 1, self.__maxy - 1, self.__maxx - 1)
            self.__opt_win.edit(er)
        except:
            pass

        curses.doupdate()

######################

if __name__ == "__main__":
    help(NCTM_Run)
