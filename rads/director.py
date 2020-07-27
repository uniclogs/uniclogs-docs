#should be in latest python library
import curses
import time
import datetime
import random

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, \
                       UniqueConstraint, \
                       ForeignKeyConstraint, \
                       Boolean, \
                       Integer, \
                       Float, \
                       Text, \
                       DateTime, \
                       create_engine
from sqlalchemy.ext.declarative import declarative_base
from loguru import logger
import log_interface
from os import getenv
from models import *
from db_interface import *


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

def print_adrequest(stdscreen):
    """Prints main menu and updates the display to current row/option selected.

    Parameters
    stdscreen : window object
        A windows object initialized by curses.initscr() from the curses library.
    ----------
    Returns
    -------
    None
    """
    ad_index = 0
    stdscreen.nodelay(True)
    stdscreen.scrollok(True)      # Enable window scroll
    stdscreen.refresh()
    loop = True
    #gets the max height and width
    height, width = stdscreen.getmaxyx()
    width -= 1
    draw_height = height - 2

    panel = curses.newpad(height, width)
    adrequest = query_new_requests()
    adrequest.insert(0, RequestHeader) #TODO fix this
    time.sleep(0.1)
    #panel.refresh(schedule_index, 0, 1, 1, draw_height, width)

    while loop == True:
        #interprets arrow key strokes
        key = stdscreen.getch()
        curses.flushinp()
        #menu navigation
        #lower bound case
        if key == curses.KEY_UP and ad_index > 0:
            ad_index-=1
        #upper bound case
        elif key == curses.KEY_DOWN and ad_index < len(adrequest)-1:
            ad_index_index += 1
        elif(key == curses.KEY_BACKSPACE):
            loop = False
        elif key == curses.KEY_F1:
            stdscreen.clear()
            stdscreen.addstr(0, 0, "You have pressed the F1 key!")
            stdscreen.refresh()
            stdscreen.getch()
        elif key == curses.KEY_F4:
            stdscreen.clear()
            stdscreen.addstr(0, 0, "You have pressed the F4 key!")
            stdscreen.refresh()
            stdscreen.getch()


        if(len(adrequest) >= (height - 2)):
            height = height*2
            panel.resize(height, width)
            panel.clear()

       # print_pad(panel, stdscreen, list1, schedule_index)

        if(len(adrequest) < (height - 2)):
        #enumerate loops over menu and creates a counter to know what part of the menu is selected
            for index, row in enumerate(adrequest):
                if index == ad_index:
                    panel.attron(curses.color_pair(1))
                panel.addstr(index + 1, 1, str(row))
                panel.attroff(curses.color_pair(1))

        panel.box()
        panel.addstr(0, 1, "Approve Deny")
        panel.refresh(ad_index, 0, 1, 1, draw_height, width)
        time.sleep(0.1)
    stdscreen.refresh()
    stdscreen.scrollok(False)      # Enable window scroll
    stdscreen.nodelay(False)

def print_schedulepad(stdscreen):
    """Prints main menu and updates the display to current row/option selected.

    Parameters
    ----------
    stdscreen : window object
        A windows object initialized by curses.initscr() from the curses library.
    menu : list
        A list containing all the items in a given request query
    Returns
    -------
    None
    """

    stdscreen.nodelay(True)
    stdscreen.scrollok(True)      # Enable window scroll
    stdscreen.refresh()
    schedule_index = 0
    loop = True
    #gets the max height and width
    height, width = stdscreen.getmaxyx()
    width -= 1
    draw_height = height - 2

    panel = curses.newpad(height, width)
    schedule = query_upcomming_requests()
    schedule.insert(0, RequestHeader) # TODO fix this
    #panel.refresh(schedule_index, 0, 1, 1, draw_height, width)

    while loop == True:
        #interprets arrow key strokes
        key = stdscreen.getch()
        curses.flushinp()
        #menu navigation
        #lower bound case
        if key == curses.KEY_UP and schedule_index > 0:
            schedule_index-=1
        #upper bound case
        elif key == curses.KEY_DOWN and schedule_index < len(schedule)-1:
            schedule_index += 1
        elif(key == curses.KEY_BACKSPACE):
            loop = False

        if(len(schedule) >= (height - 2)):
            height = height*2
            panel.resize(height, width)
            panel.clear()

       # print_pad(panel, stdscreen, list1, schedule_index)

        if(len(schedule) < (height - 2)):
        #enumerate loops over menu and creates a counter to know what part of the menu is selected
            for index, row in enumerate(schedule):
                if index == schedule_index:
                    panel.attron(curses.color_pair(1))
                panel.addstr(index + 1, 1, str(row))
                panel.attroff(curses.color_pair(1))

        panel.box()
        #panel.addstr(0, 1, "User_Token Is_Approved Is_Sent Pass_ID Created_Date Last_Modified Observation_Type Pass_Start_time")
        panel.addstr(0, 1, "Upcoming Pass Schedule")
        panel.refresh(schedule_index, 0, 1, 1, draw_height, width)
        time.sleep(0.1)
    #panel.endwin()
    stdscreen.refresh()
    stdscreen.scrollok(False)      # Enable window scroll
    stdscreen.nodelay(False)

#function to print schedule of upcoming requests
def schedule(stdscreen):
    """Prints main menu and updates the display to current row/option selected.

    Parameters
    stdscreen : window object
        A windows object initialized by curses.initscr() from the curses library.
    ----------
    Returns
    -------
    None
    """
    schedule_index = 0
    stdscreen.clear()
    #test list
   # list1 = ['op1','op2','op3','op4','op5','op6','op7','op8','op9','op10']
#    schedule = list(scheduleSelect())
    #print_menu(stdscreen, schedule, 0)
    #print(schedule)
#    vheight, vwidth = stdscreen.getmaxyx()
    #width -= 1
    #draw_height = height -2
#    panel = curses.newpad(vheight, vwidth)
    print_schedulepad(stdscreen)

#function to print accepted/denied requests
def print_archive(stdscreen):
    """Prints main menu and updates the display to current row/option selected.

    Parameters
    stdscreen : window object
        A windows object initialized by curses.initscr() from the curses library.
    ----------
    Returns
    -------
    None
    """
    archive_index = 0
    stdscreen.nodelay(True)
    stdscreen.scrollok(True)      # Enable window scroll
    stdscreen.refresh()
    loop = True
    #gets the max height and width
    height, width = stdscreen.getmaxyx()
    width -= 1
    draw_height = height -2

    panel = curses.newpad(height, width)
    archive = query_archived_requests()
    archive.insert(0, RequestHeader) # TODO fix this
    time.sleep(0.1)
    #panel.refresh(schedule_index, 0, 1, 1, draw_height, width)

    while loop == True:
        #interprets arrow key strokes
        key = stdscreen.getch()
        curses.flushinp()
        #menu navigation
        #lower bound case
        if key == curses.KEY_UP and archive_index > 0:
            archive_index-=1
        #upper bound case
        elif key == curses.KEY_DOWN and archive_index < len(archive)-1:
            archive_index += 1
        elif(key == curses.KEY_BACKSPACE):
            loop = False

        if(len(archive) >= (height - 2)):
            height = height*2
            panel.resize(height, width)
            panel.clear()

       # print_pad(panel, stdscreen, list1, schedule_index)

        if(len(archive) < (height - 2)):
        #enumerate loops over menu and creates a counter to know what part of the menu is selected
            for index, row in enumerate(archive):
                if index == archive_index:
                    panel.attron(curses.color_pair(1))
                panel.addstr(index + 1, 1, str(row))
                panel.attroff(curses.color_pair(1))

        panel.box()
        panel.addstr(0, 1, "Archives")
        panel.refresh(archive_index, 0, 1, 1, draw_height, width)
        time.sleep(0.1)
    #panel.endwin()
    stdscreen.refresh()
    stdscreen.scrollok(False)      # Enable window scroll
    stdscreen.nodelay(False)

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
    #stdscreen.nodelay(True)

    #menu options
    #menu = ['Approve/Deny Request', 'Create Request', 'Check Schedule', 'Archive', 'Exit']
    menu = ['Approve/Deny Request', 'Check Schedule', 'Archive', 'Exit']
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
        elif key == curses.KEY_F1:
            stdscreen.clear()
            stdscreen.addstr(0, 0, "You have pressed the F1 key!")
            stdscreen.refresh()
            stdscreen.getch()
        #all possible values that enter key might be depending on keyboard
        elif key == curses.KEY_ENTER or key in [10,13]:
            #code for selecting menu from menu list options 0 = Approve/Deny, 1 = Check Schedule, 2 =  Archive, 3 = Exit 
            if current_row_index == 0:
                print_adrequest(stdscreen)
            #check schedule
            if current_row_index == 1:
                schedule(stdscreen)
            if current_row_index == 2:
                print_archive(stdscreen)
            #code that terminates the program after selecting exit
            if current_row_index == len(menu)-1:
                stdscreen.addstr(0, 0, "Program successfully closed!")
                logger.info("Program successfully closed!")
                stdscreen.refresh()
                time.sleep(0.75)
                break

        #update menu change
        #time.sleep(0.1)
        print_menu(stdscreen, menu, current_row_index)
        stdscreen.refresh()

#curses.wrapper(main)
    #Restore default
    curses.echo() #Enable user input echo
    curses.nocbreak() #Enable line buffering
    curses.curs_set(True) #Enable the cursor display
    curses.resetty() # Restore terminal state
    stdscreen.keypad(False)
    #stdscreen.nodelay(False)
    curses.endwin() #Destroy virtual screen


if __name__ == '__main__':
    main();
