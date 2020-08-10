import curses
from time import sleep
from request_table import RequestTable
from eb_pass_table import EBPassTable
import sys
sys.path.append('../..')
from pass_calculator.calculator import overlap

# To prevent screen flickering
PSU_LAT = 45.512778
PSU_LONG = -122.685278
PSU_ELEV = 47.0

_DT_STR_FORMAT = "%Y/%m/%d %H:%M:%S"
_STR_FORMAT = "{:7} | {:8} | {:15} | {:^5} | {:7} | {:19} | {:19} | {:30}"
REQUEST_HEADER = "{:>7} | {:8} | {:15} | {:5} | {:7} | {:19} | {:19} | {:30}".format(
        "ID", "Status", "Type", "Sent", "Pass ID", "AOS", "LOS", "City, State")


def max_list_len(data):
    length = 0

    for d in data:
        temp = len(d)
        if temp > length:
            length = temp

    return length


def print_eb_passes(stdscreen):
    stdscreen.nodelay(True)
    stdscreen.scrollok(True)      # Enable window scroll
    stdscreen.refresh()

    screen_height, screen_width = stdscreen.getmaxyx()

    # to turn these from size to index
    screen_width -= 1
    screen_height -= 1

    screen_title_heigth = 2
    boarder_x = 1
    boarder_y = 1
    panel_space_width = 5
    pads_y0 = screen_title_heigth + boarder_y
    pads_y1 = screen_height - boarder_y

    # pass pad location on window (left panel)
    pass_win_x0 = boarder_x
    pass_win_x1 = pass_win_x0 + 50

    # schedule pad location on window (right panel)
    schedule_win_x0 = pass_win_x1 + 1 + panel_space_width
    schedule_win_x1 = screen_width - boarder_x

    eb_passes = EBPassTable()
    pass_pad_height = len(eb_passes)
    pass_pad_width = len(str(eb_passes[0]))
    pass_pad = curses.newpad(pass_pad_height+1, pass_pad_width+1)

    schedule = RequestTable()
    schedule_pad_height = len(schedule)
    schedule_pad_width = len(str(schedule[0]))
    schedule_pad = curses.newpad(schedule_pad_height+1, schedule_pad_width+1)

    focus = 0
    pass_index = 0
    schedule_index = 0

    pass_pad.refresh(pass_index, 0, pads_y0, pass_win_x0, pads_y1, pass_win_x1)
    schedule_pad.refresh(schedule_index, 0, pads_y0, schedule_win_x0, pads_y1, schedule_win_x1)

    msg = "EB Pass Scheduler (lat {}, long {}, elev {} meters)".format(PSU_LAT, PSU_LONG, PSU_ELEV)
    stdscreen.addstr(0, screen_width//2 - len(msg)//2, msg)
    stdscreen.addstr(2, boarder_x, eb_passes.header)
    stdscreen.addstr(2, pass_win_x1+panel_space_width, " "+schedule.header)

    running = True
    while(running is True):
        key = stdscreen.getch()
        curses.flushinp()

        if key == ord('f'):  # swap focus onto other pad
            focus = (focus + 1) % 2
        elif key == ord('c'):  # clear and quit
            running = False
        elif key == ord('s'):  # save and quit
            running = False
            eb_passes.save()
            schedule.save()

        if focus == 0:
            if key == curses.KEY_UP and pass_index > 0:
                pass_index -= 1
            elif key == curses.KEY_DOWN and pass_index < pass_pad_height-1:
                pass_index += 1
            elif key == ord('a'):  # add new uniclogs pass
                eb_passes[pass_index].add = True
                for i in range(schedule_pad_height):
                    if overlap(eb_passes[pass_index], schedule[i].pass_data) is True:
                        schedule[i].deny()
            elif key == ord('d'):  # remove new uniclogs pass
                eb_passes[pass_index].add = False
                for i in range(schedule_pad_height):
                    if overlap(eb_passes[pass_index], schedule[i].pass_data) is True:
                        schedule[i].undeny()

            # rebuild display strings for eb_passes
            for i in range(pass_index, pass_pad_height):
                if i == pass_index:  # current index
                    pass_pad.addstr(i, 0, str(eb_passes[i]), curses.color_pair(1))
                elif eb_passes[i].add is True:  # added
                    pass_pad.addstr(i, 0, str(eb_passes[i]), curses.color_pair(3))
                else:
                    pass_pad.addstr(i, 0, str(eb_passes[i]))

            # rebuild display strings for schedule
            for i in range(schedule_index, schedule_pad_height):
                if overlap(eb_passes[pass_index], schedule[i].pass_data) is True:
                    schedule_pad.addstr(i, 0, str(schedule[i]), curses.color_pair(5))
                elif schedule[i].is_approved is False:  # denied
                    schedule_pad.addstr(i, 0, str(schedule[i]), curses.color_pair(2))
                else:
                    schedule_pad.addstr(i, 0, str(schedule[i]))
        else:
            if key == curses.KEY_UP and schedule_index > 0:
                schedule_index -= 1
            elif key == curses.KEY_DOWN and schedule_index < schedule_pad_height-1:
                schedule_index += 1

            # rebuild display strings for eb_passes
            for i in range(pass_index, pass_pad_height):
                if overlap(schedule[schedule_index].pass_data, eb_passes[i]) is True:
                    pass_pad.addstr(i, 0, str(eb_passes[i]), curses.color_pair(4))
                elif eb_passes[i].add is True:  # added
                    pass_pad.addstr(i, 0, str(eb_passes[i]), curses.color_pair(3))
                else:
                    pass_pad.addstr(i, 0, str(eb_passes[i]))

            # rebuild display strings for schedule
            for i in range(schedule_index, schedule_pad_height):
                if i == schedule_index:  # current index
                    schedule_pad.addstr(i, 0, str(schedule[i]), curses.color_pair(1))
                elif schedule[i].is_approved is False:  # denied
                    schedule_pad.addstr(i, 0, str(schedule[i]), curses.color_pair(2))
                else:
                    schedule_pad.addstr(i, 0, str(schedule[i]))

        pass_pad.refresh(pass_index, 0, pads_y0, pass_win_x0, pads_y1, pass_win_x1)
        schedule_pad.refresh(schedule_index, 0, pads_y0, schedule_win_x0, pads_y1, schedule_win_x1)

        sleep(0.01)

    stdscreen.refresh()
    stdscreen.scrollok(False)      # Enable window scroll
    stdscreen.nodelay(False)
