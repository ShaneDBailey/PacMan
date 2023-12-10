#Shane Bailey, Nick Ford
#file to store constants, convention purposes
BOARD_WIDTH=630
BOARD_HEIGHT = 690
BOARD_GRID_SIZEX = 21
BOARD_GRID_SIZEY = 23
TILESIZE = BOARD_WIDTH // BOARD_GRID_SIZEX

FRAME_RATE = 60

DOTS = 0
WALLS = 1
SPACE = 2
BIGDOTS = 3
PACMAN = 4

YELLOW = 5
RED = 6
PINK = 7
BLUE = 8

LEFT_PORTAL = 9
RIGHT_PORTAL = 10

LEFT_PORTAL_POSITION = (0,10)
RIGHT_PORTAL_POSITION = (20,10)

RED_TARGET = (24,-2)
PINK_TARGET = (0,-2)
BLUE_TARGET = (24,28)
YELLOW_TARGET = (0,28)


CHARACTER_SPACES = (0,3,4)
GHOST_SPACES = (0,3,4,6,5,7,8,9,10)
PORTAL_SPACES = (9,10)