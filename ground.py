import pygame
from globals import GAME_WIDTH, HIT_BOXES

class Ground:

    def __init__(self, x) -> None:
        self.x = x
        self.y = 375
        self.sprite = pygame.transform.scale_by(pygame.image.load(f"assets/ground.png").convert_alpha(), 3)
        self.rect = pygame.Rect((self.x, self.y), (GAME_WIDTH, self.sprite.get_height()))

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y-30))

        if HIT_BOXES: pygame.draw.rect(screen, "blue", self.rect, 2)

    def move(self, speed):
        self.x -= speed
        if self.x < - self.sprite.get_width(): self.x += 2*self.sprite.get_width()-100

    def collide(self, dino):
        if self.rect.colliderect(dino.rect):
            dino.y = 329
            return True