import sys
sys.path.insert(0, '../src')
from models import Tle, Session


TEST_TLE_HEADER = "ISS (ZARYA)"
TEST_TLE_LINE_1 = "1 25544U 98067A   20199.71986111 -.00000291  00000-0  28484-5 0  9999"
TEST_TLE_LINE_2 = "2 25544  51.6429 197.3485 0001350 125.7534 225.4894 15.49513771236741"


def add_tle():
    session = Session()
    new_tle = Tle(
            header_text=TEST_TLE_HEADER,
            first_line=TEST_TLE_LINE_1,
            second_line=TEST_TLE_LINE_2
            )

    session.add(new_tle)
    session.commit()
    session.close()


if __name__ == '__main__':
    add_tle()
