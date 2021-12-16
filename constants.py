from enum import Enum;
from point import Point;

import scipy.constants as spc;

class Colors(Enum):
    '''
    Enum for color values
    '''

    WHITE: str = '#FFFFFF';
    GREEN_YELLOW: str = '#ADFF2F';
    LIGHT_SEA_GREEN: str = '#20B2AA';
    GRAY: str = '#333333';
    LIGHT_GRAY: str = '#A9A9A9';
    DARK_GRAY: str = '#212121';
    DARK_RED: str = '#3D0103';
    ORANGE: str = '#FF8000';

HEIGHT: int = 600;
WIDTH:  int = 600;

TOPMOST:    Point = Point(WIDTH * 0.5, 0);
BOTTOMMOST: Point = Point(WIDTH * 0.5, HEIGHT);
LEFTMOST:   Point = Point(0, HEIGHT * 0.5);
RIGHTMOST:  Point = Point(WIDTH, HEIGHT * 0.5);

CENTER: Point = Point(WIDTH * 0.5, HEIGHT * 0.5);
RAYLENGTH: int = 250;

SPEED_OF_LIGHT = spc.speed_of_light / 1000.0;