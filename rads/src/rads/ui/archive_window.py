"""
The window for see all archive requests.
"""

import curses
import time
from rads.database.query import query_archived_requests
from rads.database.request_data import RequestHeader

# To prevent screen flickering
WAIT_TIME = 0.07


def print_archive(stdscreen):
    """Prints archive menu and updates the display to current row/option selected.

    function to print accepted/denied requests

    Parameters
    ----------
    stdscreen : window object
        A windows object initialized by curses.initscr() from the curses
        library.
    """
    archive_index = 0
    stdscreen.nodelay(True)
    stdscreen.scrollok(True)      # Enable window scroll
    stdscreen.refresh()
    loop = True
    # gets the max height and width
    height, width = stdscreen.getmaxyx()
    width -= 1
    draw_height = height - 2

    panel = curses.newpad(height, width)
    archive = query_archived_requests()

    while loop is True:
        # interprets arrow key strokes
        key = stdscreen.getch()
        curses.flushinp()
        # menu navigation
        # lower bound case
        if key == curses.KEY_UP and archive_index > 0:
            archive_index -= 1
        # upper bound case
        elif key == curses.KEY_DOWN and archive_index < len(archive)-1:
            archive_index += 1
        elif key == ord('c') or key == ord('s'):  # Exit
            loop = False

        if len(archive) >= (height - 2):
            height = height*2
            panel.resize(height, width)

        if len(archive) < (height - 2):
            # enumerate loops over menu and creates a counter to know what part
            # of the menu is selected
            for index, row in enumerate(archive):
                if index == archive_index:
                    panel.attron(curses.color_pair(1))
                panel.addstr(index + 1, 1, str(row))
                panel.attroff(curses.color_pair(1))

        description = "Archives(Ordered BY AOS DESC)"
        stdscreen.addstr(0, (width+1)//2 - len(description)//2, description)
        info = "Arrow Keys: To Move, c or s: Exit"
        stdscreen.addstr(1, (width+1)//2 - len(info)//2, info)
        stdscreen.addstr(3, 2, RequestHeader)
        stdscreen.addstr(2, 0, " ")
        panel.refresh(archive_index, 0, 3, 1, draw_height, width)
        stdscreen.refresh()
        time.sleep(WAIT_TIME)

    stdscreen.refresh()
    stdscreen.scrollok(False)      # Enable window scroll
    stdscreen.nodelay(False)
