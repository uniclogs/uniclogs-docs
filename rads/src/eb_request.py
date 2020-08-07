import curses
import time
import sys
from loguru import logger
from datetime import datetime, timezone, timedelta
from db_interface import query_upcomming_requests
sys.path.insert(0, '../..')
from pass_calculator.calculator import get_all_passes, pass_overlap


#To prevent screen flickering
WAIT_TIME = 0.07
TEST_TLE_HEADER = "ISS (ZARYA)"
TEST_TLE_LINE_1 = "1 25544U 98067A   20199.71986111 -.00000291  00000-0  28484-5 0  9999"
TEST_TLE_LINE_2 = "2 25544  51.6429 197.3485 0001350 125.7534 225.4894 15.49513771236741"
PSU_LAT = 45.512778
PSU_LONG = -122.685278
PSU_ELEV = 47.0
_DT_STR_FORMAT = "%Y/%m/%d %H:%M:%S"


def print_eb_passes(stdscreen):
    """Prints main menu and updates the display to current row/option selected.

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
    # tle = query_tle()
    tle = [TEST_TLE_LINE_1, TEST_TLE_LINE_2]
    now = datetime.utcnow()
    now = now.replace(tzinfo=timezone.utc)
    future = datetime.now() + timedelta(days=7)
    future = future.replace(tzinfo=timezone.utc)
    passes = get_all_passes(
            tle,
            PSU_LAT,
            PSU_LONG,
            now,
            future
            )

    approved_req = query_upcomming_requests()

    archive = []
    for p in passes:
        overlap = ""
        for a in approved_req:
            a.pass_data.aos_utc = a.pass_data.aos_utc.replace(tzinfo=timezone.utc)
            a.pass_data.los_utc = a.pass_data.los_utc.replace(tzinfo=timezone.utc)
            if pass_overlap(p, [a.pass_data]) is True:
                print("overlap")
                overlap += str(a.id) + ", "

        pass_str = "{} | {} | {}".format(
                p.aos_utc.strftime(_DT_STR_FORMAT),
                p.los_utc.strftime(_DT_STR_FORMAT),
                overlap
                )
        archive.append(pass_str)

    # archive.insert(0, RequestHeader) # TODO fix this
    # panel.refresh(schedule_index, 0, 1, 1, draw_height, width)
    # panel.box()
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
        elif(key == 99 or key == 115):  # c = 99 s = 115 Exit
            loop = False

        if(len(archive) >= (height - 2)):
            height = height*2
            panel.resize(height, width)
            # panel.clear()
            # panel.refresh(schedule_index, 0, 2, 1, draw_height, width)
        # print_pad(panel, stdscreen, list1, schedule_index)

        if(len(archive) < (height - 2)):
            """
            enumerate loops over menu and creates a counter to know what part
            of the menu is selected.
            """
            for index, row in enumerate(archive):
                if index == archive_index:
                    panel.attron(curses.color_pair(1))
                panel.addstr(index + 1, 1, str(row))
                panel.attroff(curses.color_pair(1))

        # panel.box()
        msg = "PSU engineering building at lat {}, long {}, elev {} meters".format(PSU_LAT, PSU_LONG, PSU_LONG)
        stdscreen.addstr(0, (width+1)//2 - len(msg)//2, msg)
        info = "Arrow Keys: To Move, c or s: Exit"
        stdscreen.addstr(1, (width+1)//2 - len(info)//2, info)
        RequestHeader = "{:19} | {:19}".format("AOS", "LOS")
        stdscreen.addstr(3, 2, RequestHeader)
        stdscreen.addstr(2, 0, " ")
        panel.refresh(archive_index, 0, 3, 1, draw_height, width)
        stdscreen.refresh()
        time.sleep(WAIT_TIME)

    # panel.endwin()
    stdscreen.refresh()
    stdscreen.scrollok(False)      # Enable window scroll
    stdscreen.nodelay(False)


