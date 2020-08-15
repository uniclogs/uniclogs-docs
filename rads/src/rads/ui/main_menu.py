"""
The main menu for rads.
"""

import curses
import time
from loguru import logger
from rads.log_interface import init
from .approve_deny_window import print_adrequest
from .schedule_window import print_schedulepad
from .archive_window import print_archive
from .eb_request_window import print_eb_passes

# To prevent screen flickering
WAIT_TIME = 0.07


def init_ui(stdscreen):
    """
    initialize curses.
    """

    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_YELLOW)

    # curses configuration
    curses.savetty()  # save the terminal state
    curses.noecho()  # disable user input echo
    curses.cbreak()  # disable line buffering
    curses.curs_set(False)  # disable the cursor display
    stdscreen.keypad(True)


def end_ui(stdscreen):
    """
    End ncurses.
    """

    # Restore default
    curses.echo()           # Enable user input echo
    curses.nocbreak()       # Enable line buffering
    curses.curs_set(True)   # Enable the cursor display
    curses.resetty()        # Restore terminal state
    stdscreen.keypad(False)
    curses.endwin()         # Destroy virtual screen


def main_menu(stdscreen):
    """
    The main for rads.
    """

    # menu options
    menu = ['Approve/Deny Request', 'Check Schedule', 'Archive', 'EB passes', 'Exit']
    current_row_index = 0

    # loop to contstantly print the menu screen and refresh
    while True:
        stdscreen.clear()
        # gets the max height and width
        h, w = stdscreen.getmaxyx()

        # enumerate loops over menu and creates a counter to know what part of the
        # menu is selected
        for index, row in enumerate(menu):
            # X is equal to center of screen with text alignment of the x axis
            x = w//2 - len(row)//2
            # y is equal to the center of the screen of the axis
            y = h//2 - len(menu)//2 + index
            # highlights the selected text
            if index == current_row_index:
                stdscreen.attron(curses.color_pair(1))
                stdscreen.addstr(y, x, row)
                stdscreen.attroff(curses.color_pair(1))
            # adds menu text not selected
            else:
                stdscreen.addstr(y, x, row)

        stdscreen.refresh()

        # interprets arrow key strokes
        key = stdscreen.getch()
        stdscreen.clear()

        # menu navigation
        # lower bound case
        if key == curses.KEY_UP and current_row_index > 0:
            current_row_index -= 1
        # upper bound case
        elif key == curses.KEY_DOWN and current_row_index < len(menu)-1:
            current_row_index += 1
        # all possible values that enter key might be depending on keyboard
        elif key == curses.KEY_ENTER or key in [10, 13]:
            # code for selecting menu from menu list options
            # 0 = Approve/Deny, 1 = Check Schedule, 2 =  Archive, 3 = Exit
            if current_row_index == 0:
                print_adrequest(stdscreen)
            elif current_row_index == 1:
                print_schedulepad(stdscreen)
            elif current_row_index == 2:
                print_archive(stdscreen)
            elif current_row_index == 3:
                print_eb_passes(stdscreen)
            # code that terminates the program after selecting exit
            if current_row_index == len(menu)-1:
                stdscreen.addstr(0, 0, "Program successfully closed!")
                logger.info("Program successfully closed!")
                stdscreen.refresh()
                time.sleep(0.75)
                break


def main():
    """
    Main for rads.
    """
    msg = None

    init('rads')
    logger.info('Starting director')
    stdscreen = curses.initscr()

    init_ui(stdscreen)

    try:
        main_menu(stdscreen)
    except KeyboardInterrupt:
        msg = "control-c was called"
    #except Exception as e:
    #    msg = "exception caught: {}".format(e)
    #    logger.error(msg)

    end_ui(stdscreen)

    if msg is not None:
        print(msg)
