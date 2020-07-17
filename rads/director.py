#should be in latest python library
import curses
import time
from loguru import logger
from .log_interface import *


#function to print the menu taking in a the standard screen and default row index 0
def print_menu(stdscreen,menu, current_row_index):
    """Prints main menu and updates the display to current row/option selected.

    Parameters
    ----------
    stdscreen : window object
        A windows object initialized by curses.initscr() from the curses library.
    menu: list 
        A list that contains all text for the main menu options.
    current_row_index: int
        The current index row number of the current menu option selected.
    Returns
    -------
    None
    """

    stdscreen.clear()
    #gets the max height and width
    h, w = stdscreen.getmaxyx()

    #enumerate loops over menu and creates a counter to know what part of the menu is selected
    for index, row in enumerate(menu):
        #X is equal to center of screen with text alignment of the x axis
        x = w//2 - len(row)//2
        #y is equal to the center of the screen of the axis
        y = h//2 - len(menu)//2 + index
        #highlights the selected text
        if index == current_row_index:
            stdscreen.attron(curses.color_pair(1))
            stdscreen.addstr(y, x, row)
            stdscreen.attroff(curses.color_pair(1))
        #adds menu text not selected
        else:
            stdscreen.addstr(y, x, row)

    stdscreen.refresh()

def main():

    log_interface.init('rads')
    logger.info('Starting director')
    stdscreen = curses.initscr()
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    #curses configuration
    curses.savetty() #save the terminal state
    curses.noecho() #disable user input echo
    curses.cbreak() #disable line buffering
    curses.curs_set(False) #disable the cursor display
    stdscreen.keypad(True)

    #menu options
    menu = ['Approve/Deny Request', 'Create Request', 'Check Schedule', 'Archive', 'Exit']
    current_row_index = 0
    print_menu(stdscreen, menu, current_row_index)

    #loop to contstantly print the menu screen and refresh
    while True:
        #interprets arrow key strokes
        key = stdscreen.getch()
        stdscreen.clear()

        #menu navigation
        #lower bound case
        if key == curses.KEY_UP and current_row_index > 0:
            current_row_index -=1
        #upper bound case
        elif key == curses.KEY_DOWN and current_row_index < len(menu)-1:
            current_row_index += 1
        #all possible values that enter key might be depending on keyboard
        elif key == curses.KEY_ENTER or key in [10,13]:
            #temporary code for selecting menu options other then exit
            if current_row_index < len(menu)-1:
                stdscreen.clear()
                stdscreen.addstr(0, 0, "You Selected {}".format(menu[current_row_index]))
                stdscreen.refresh()
                stdscreen.getch()
            #code that terminates the program after selecting exit
            if current_row_index == len(menu)-1:
                stdscreen.addstr(0, 0, "Program successfully closed!")
                logger.info("Program successfully closed!")
                stdscreen.refresh()
                time.sleep(0.75)
                break

        #update menu change
        print_menu(stdscreen, menu, current_row_index)
        stdscreen.refresh()

#curses.wrapper(main)
    #Restore default
    curses.echo() #Enable user input echo
    curses.nocbreak() #Enable line buffering
    curses.curs_set(True) #Enable the cursor display
    curses.resetty() # Restore terminal state
    stdscreen.keypad(False)
    curses.endwin() #Destroy virtual screen


if __name__ == '__main__':
    main();
