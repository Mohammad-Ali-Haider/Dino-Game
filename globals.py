import pygame

pygame.init()
pygame.mixer.init()

GAME_WIDTH = 800
GAME_HEIGHT = 450
SPEED = 7.5
GRAVITY = 2 * 10000
JUMP_VEL = 0.8 * 1000
HIT_BOXES = False
TYPES = ["cactus", "bird"]
TYPE_SPRITE = [[pygame.image.load(f"assets/cacti/cactus1.png"),pygame.image.load(f"assets/cacti/cactus2.png"),pygame.image.load(f"assets/cacti/cactus3.png"),pygame.image.load(f"assets/cacti/cactus4.png"),pygame.image.load(f"assets/cacti/cactus5.png"),pygame.image.load(f"assets/cacti/cactus6.png")], [pygame.image.load(f"assets/Ptero1.png"),pygame.image.load(f"assets/Ptero2.png")]]
LEVELS_OF_FLIGHT = [5, 35, 50]
FONT = pygame.font.Font(f"assets/PressStart2P-Regular.ttf", 16)

jump = pygame.mixer.Sound(f"assets/sfx/jump.mp3")
lost = pygame.mixer.Sound(f"assets/sfx/lose.mp3")
points = pygame.mixer.Sound(f"assets/sfx/100points.mp3")

OBSTICLES = list(zip(TYPES, TYPE_SPRITE))