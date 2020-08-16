"""
The window for see the schedule for oresat's missions.
"""

import curses
import time
from loguru import logger
from rads.database.query import query_upcomming_requests
from rads.database.update import update_approve_deny
from rads.database.request_data import RequestHeader
from rads.command.schedule_pass import Schedule_Pass

# To prevent screen flickering
WAIT_TIME = 0.07


def print_schedulepad(stdscreen):
    """Prints schedule and updates the display to current row/option selected.
    Allows for cancellation of approved requests.

    Parameters
    ----------
    stdscreen : window object
        A windows object initialized by curses.initscr() from the curses
        library.
    """

    stdscreen.nodelay(True)
    stdscreen.scrollok(True)  # Enable window scroll
    stdscreen.refresh()
    schedule_index = 0
    loop = True
    # gets the max height and width
    height, width = stdscreen.getmaxyx()
    width -= 1
    draw_height = height - 2

    panel = curses.newpad(height, width)
    schedule = query_upcomming_requests()

    while loop is True:
        # interprets key strokes
        key = stdscreen.getch()
        curses.flushinp()

        # menu navigation

        # lower bound case
        if key == curses.KEY_UP and schedule_index > 0:
            schedule_index -= 1
        # upper bound case
        elif key == curses.KEY_DOWN and schedule_index < len(schedule)-1:
            schedule_index += 1
        elif key == ord('c'):  # 99:  # c = 99 Exit without Saving
            loop = False
        elif key == ord('s'):  # 115:  # s = 115 Exit and Save
            loop = False
            update_approve_deny(schedule)
            # UPDATE to connect to COSMOS
            try:
                schedule_pass = Schedule_Pass(schedule)
                schedule_pass.schedule_all()
            except Exception as e:
                logger.error("cosmos command interface failed with: {}".format(e))
        elif key == ord('a'):  # 97:  # a = 97
            schedule[schedule_index].is_approved = True
            panel.touchwin()
        elif key == ord('d'):  # 100:  # d = 100
            schedule[schedule_index].is_approved = False
            panel.touchwin()

        if len(schedule) >= (height - 2):
            height = height*2
            panel.resize(height, width)
        else:
            # enumerate loops over menu and creates a counter to know what part
            # of the menu is selected
            for index, row in enumerate(schedule):
                if index == schedule_index:
                    panel.attron(curses.color_pair(1))
                panel.addstr(index + 1, 1, str(row))
                panel.attroff(curses.color_pair(1))
                if schedule[index].is_approved is False:
                    panel.attron(curses.color_pair(2))
                    panel.addstr(index + 1, 1, str(row))
                    panel.attroff(curses.color_pair(2))

        description = "Upcoming Pass Schedule(Ordered By AOS ASC)"
        stdscreen.addstr(0, (width+1)//2 - len(description)//2, description)
        info = "Arrow Keys: To Move, a: Accept, d: Deny, c: Exit,\
                s: Save and Exit"
        stdscreen.addstr(1, (width+1)//2 - len(info)//2, info)
        stdscreen.addstr(3, 2, RequestHeader)
        stdscreen.addstr(2, 0, " ")
        panel.refresh(schedule_index, 0, 3, 1, draw_height, width)
        stdscreen.refresh()
        time.sleep(WAIT_TIME)

    stdscreen.refresh()
    stdscreen.scrollok(False)  # Enable window scroll
    stdscreen.nodelay(False)
