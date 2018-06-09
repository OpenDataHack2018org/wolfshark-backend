from enum import Enum
from Magics.macro import *


class Areas(Enum):
    WORLD = mmap()
    EUROPE = mmap(
        subpage_lower_left_latitude    = 21.51,
        subpage_lower_left_longitude   = -37.27,
        subpage_projection             = "polar_stereographic",
        subpage_upper_right_latitude   = 51.28,
        subpage_upper_right_longitude  = 65,
        subpage_map_vertical_longitude = 0)
    AUSTRALIA = mmap(
        subpage_upper_right_longitude  = 190.00,
        subpage_upper_right_latitude   = -5.00,
        subpage_lower_left_latitude    = -55.00,
        subpage_lower_left_longitude   = 80.00,
        subpage_map_projection         = "cylindrical")
    N_AMERICA = mmap(
        subpage_upper_right_longitude  = -15.00,
        subpage_upper_right_latitude   = 30.00,
        subpage_lower_left_latitude    = -5.00,
        subpage_map_vertical_longitude = -100.00,
        subpage_lower_left_longitude   = -140.00,
        subpage_map_projection         = "polar_stereographic")
    AFRICA = mmap(
        subpage_lower_left_latitude    = -40,
        subpage_lower_left_longitude   = -45,
        subpage_projection             = "cylindrical",
        subpage_upper_right_latitude   = 40,
        subpage_upper_right_longitude  = 75)
    ASIA = mmap(
        subpage_lower_left_latitude    = 0,
        subpage_lower_left_longitude   = 55,
        subpage_projection             = "cylindrical",
        subpage_upper_right_latitude   = 80,
        subpage_upper_right_longitude  = 175)
    S_AMERICA = mmap(
        subpage_lower_left_latitude    = -65,
        subpage_lower_left_longitude   = -125,
        subpage_projection             = "cylindrical",
        subpage_upper_right_latitude   = 20,
        subpage_upper_right_longitude  = 5)