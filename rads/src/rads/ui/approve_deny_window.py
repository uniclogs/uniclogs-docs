"""
The main menu for rads.
"""

import curses
import time
from loguru import logger
from rads.database.query import query_new_requests
from rads.database.update import update_approve_deny
from rads.database.request_data import RequestHeader
from rads.command.schedule_pass import Schedule_Pass

# To prevent screen flickering
WAIT_TIME = 0.07


def print_adrequest(stdscreen):
    """Prints accept/deny menu and updates the display to current row/option
    selected. Allow for accepting and denying requests.

    Parameters
    ----------
    stdscreen : window object
        A windows object initialized by curses.initscr() from the curses
        library.
    """
    ad_index = 0
    stdscreen.nodelay(True)
    stdscreen.scrollok(True)      # Enable window scroll
    stdscreen.refresh()
    loop = True
    # gets the max height and width
    height, width = stdscreen.getmaxyx()
    width -= 1
    draw_height = height - 2

    panel = curses.newpad(height, width)
    adrequest = query_new_requests()

    while loop is True:
        # interprets arrow key strokes
        key = stdscreen.getch()
        curses.flushinp()
        # menu navigation
        # lower bound case
        if key == curses.KEY_UP and ad_index > 0:
            ad_index -= 1
            panel.refresh(ad_index, 0, 3, 1, draw_height, width)
        # upper bound case
        elif key == curses.KEY_DOWN and ad_index < len(adrequest)-1:
            ad_index += 1
            panel.refresh(ad_index, 0, 3, 1, draw_height, width)
        elif key == ord('c'):  # Exit without Saving
            loop = False
        elif key == ord('s'):  # Exit and Save
            loop = False
            update_approve_deny(adrequest)
            # Update added to connect to COSMOS
            try:
                schedule_pass = Schedule_Pass(adrequest)
                schedule_pass.schedule_all()
            except Exception as e:
                logger.error("cosmos command interface failed with: {}".format(e))
        elif key == ord('a'):  # Approve request
            if len(adrequest[ad_index].db_approved_overlap) == 0:
                adrequest[ad_index].is_approved = True
                for index, row in enumerate(adrequest):
                    if adrequest[index].id in adrequest[ad_index].new_overlap:
                        adrequest[index].is_approved = False
            panel.touchwin()
        elif key == ord('d'):  # Deny request
            adrequest[ad_index].is_approved = False
            panel.touchwin()
        elif key == ord('w'):  # To undo Accepts
            for index, row in enumerate(adrequest):
                if adrequest[index].id in adrequest[ad_index].new_overlap:
                    adrequest[index].is_approved = None
            adrequest[ad_index].is_approved = None
            panel.touchwin()

        while len(adrequest) >= (height - 2):
            height = height*2
            panel.resize(height, width)

        for index, row in enumerate(adrequest):
            if adrequest[ad_index].is_approved is False:
                panel.attron(curses.color_pair(2))

        if len(adrequest) < (height - 2):
            # enumerate loops over menu and creates a counter to know what part
            # of the menu is selected
            for index, row in enumerate(adrequest):
                if index == ad_index:
                    panel.attron(curses.color_pair(1))
                if adrequest[ad_index].is_approved is None:
                    panel.addstr(index + 1, 1, str(row))

                if adrequest[index].is_approved is False:
                    panel.attron(curses.color_pair(2))
                    panel.addstr(index + 1, 1, str(row))
                    panel.attroff(curses.color_pair(2))
                elif adrequest[index].is_approved is True:
                    panel.attron(curses.color_pair(3))
                    panel.addstr(index + 1, 1, str(row))
                    panel.attroff(curses.color_pair(3))
                elif adrequest[index].id in adrequest[ad_index].new_overlap:
                    panel.attron(curses.color_pair(4))
                    panel.addstr(index + 1, 1, str(row))
                    panel.attroff(curses.color_pair(4))
                elif len(adrequest[index].db_approved_overlap) > 0:
                    panel.attron(curses.color_pair(5))
                    panel.addstr(index + 1, 1, str(row))
                    panel.attroff(curses.color_pair(5))
                else:
                    panel.addstr(index + 1, 1, str(row))
                    panel.attroff(curses.color_pair(1))
                panel.attroff(curses.color_pair(1))

        # overlap message
        blank = " " * width
        if len(adrequest[ad_index].db_approved_overlap) == 0:
            stdscreen.addstr(2, 0, blank)
        else:
            schedule_overlap = "Overlaps with approved Request ID: " + \
                    str(adrequest[ad_index].db_approved_overlap)
            stdscreen.addstr(2, 7, schedule_overlap)

        # main title
        description = "Accept Deny Requests(Ordered By Date Created)"
        stdscreen.addstr(0, (width+1)//2 - len(description)//2, description)

        # key layout
        info = "Arrow Keys: To Move, a: Accept, d: Deny, w:Reset to Pending c: Exit, s: Save and Exit"
        stdscreen.addstr(1, (width+1)//2 - len(info)//2, info)
        stdscreen.addstr(3, 2, RequestHeader)

        panel.refresh(ad_index, 0, 3, 1, draw_height, width)
        stdscreen.refresh()
        time.sleep(WAIT_TIME)

    stdscreen.refresh()
    stdscreen.scrollok(False)      # Enable window scroll
    stdscreen.nodelay(False)
