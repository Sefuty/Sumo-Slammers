# Window settings
WIDTH = 800  # Match your map width
HEIGHT = 600  # Match your map height
FRAME_RATE = 60

# Colors in RGB format
WHITE = (255, 255, 255)
RED = (220, 60, 60)       # More muted red
BLUE = (60, 60, 220)      # More muted blue
GREEN = (60, 179, 113)    # More pleasant green
BLACK = (30, 30, 30)      # Softer black
GRAY = (128, 128, 128)    # For UI elements
GOLD = (212, 175, 55)     # For victory effects

# Physics settings
GRAVITY = 0.6             # Faster fall
JUMP_FORCE = -12          # Stronger jump
MOVEMENT_SPEED = 6        # Faster base movement
AIR_RESISTANCE = 0.95     # More air control
FRICTION = 0.85           # Same friction

# Combat settings
BASE_KNOCKBACK = 8        # Base knockback
MAX_KNOCKBACK = 40        # Higher max knockback
PLAYER_SIZE = 30          # Slightly larger players
DAMAGE_AMOUNT = 6         # Base damage
MAX_DAMAGE = 100          # Max damage percent
RECOVERY_FRAMES = 15      # Frames where you can't take damage after hit

# Dash settings
DASH_FORCE = 18           # Dash speed
DASH_LENGTH = 10          # Dash duration
DASH_COOLDOWN = 240       # 4 seconds between each dash (60 FPS * 4)
DASH_DAMAGE_BONUS = 1.2   # Damage bonus when dashing
MAX_AIR_DASH = 1         # Keep one air dash

# Platform settings
PLATFORM_X = WIDTH * 0.15  # Adjust to match your map's platform position
PLATFORM_Y = HEIGHT * 0.75  # Adjust to match your map's platform height
PLATFORM_WIDTH = WIDTH * 0.7  # Match your map's platform width
PLATFORM_HEIGHT = 20  # Match your map's platform height

# Spawn settings
# Players are placed at the edges of the platform
# SPAWN_DISTANCE = 0 means they start exactly at the edge
SPAWN_DISTANCE = 50       # Small distance from edge so players don't slide off

# Adjust how high above the platform players start
SPAWN_HEIGHT = 150        # Fixed height above platform

# Game settings
ROUND_TIME = 60           # 1 min per round
MAX_POINTS = 3            # Points needed to win

# UI settings
LARGE_FONT = 48           # Large headers
MEDIUM_FONT = 36          # Medium text
SMALL_FONT = 24           # Small text 