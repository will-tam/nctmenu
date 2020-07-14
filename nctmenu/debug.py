from syslog import *
import curses

DBG = True

def printthis(what, val, cwin=None, lin=0, col=0):
    """
    Display a given information.
    @parameters : what = what to display.
                  val = value to display.
                  cwin = adrress of the curses window. None if normal term display.
                  lin = line where to write.
                  col = col where to write.
    @return : none.
    """
    if DBG :
        dbginfo = "\n**\n{} = {}\n**\n".format(what, val)
        if cwin:
            cwin.addstr(lin, col, dbginfo, curses.A_REVERSE)
        else:
            print(dbginfo)

def syslogthis(what, val):
    """
    Display a given information in syslog.
    @parameters : what = what to display.
                  val = value to display.
    @return : none.
    """
    syslog(LOG_DEBUG, "{0} = {1}".format(what, val))
