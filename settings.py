import math

# Game Settings
RES = WIDTH, HEIGHT = 1600, 900
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60
DARKNESS_FACTOR = 1.25

# Player Settings
PLAYER_POS = 1.5, 5 # mini_map
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002
PLAYER_HEIGHT = 0.6  # Camera height as fraction of wall height (0.5 = centered, 0.75 = upper third)
FOV = math.pi / 4
HALF_FOV = FOV / 2
NUM_RAYS = 200  # Increased to 200 for tighter spacing (8px width)
MAX_DEPTH = 20
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
SCALE = WIDTH // NUM_RAYS
PROJ_COEFF = DIST * SCALE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# ASCII Settings
# We want a font that supports unicode.
FONT_SIZE = 20
# Sorted roughly by visual density (light to dark)
# Curated list of ASCII and CJK characters
# WALL_CHARS = ' .,*"一~:;三!〢+中田国8#@'
WALL_CHARS = ' .一:三!〢+中国#@8'


