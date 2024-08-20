import pygame
import random
from globals import OBSTICLES, LEVELS_OF_FLIGHT, GAME_WIDTH, HIT_BOXES, lost

class Obsticle:

    def __init__(self, x) -> None:
        self.x = x
        self.y = 375
        self.scaleFactor = 1.25
        self.obsticle = OBSTICLES[random.randint(0, len(OBSTICLES)-1)]
        if random.randint(1, 100) > 25:
            self.obsticle = OBSTICLES[0]
            self.sprite = self.obsticle[1][random.randint(0,5)]
        else:
            self.obsticle = OBSTICLES[0]
            self.sprite = self.obsticle[1][0]
            self.y = self.y - LEVELS_OF_FLIGHT[random.randint(0,2)]
        self.sprite = pygame.transform.scale_by(self.sprite, self.scaleFactor)
        self.rect_coords = [self.sprite.get_width(), self.sprite.get_height()]
        self.rect = pygame.Rect((self.x, self.y), (self.rect_coords))

    def move(self, speed):
        self.x -= speed
        print(speed)
        self.rect = pygame.Rect((self.x, self.y-self.rect_coords[1]), (self.rect_coords))
        if self.x < -self.rect_coords[0]:
            self.y = 375
            if random.randint(1, 100) > 25:
                self.obsticle = OBSTICLES[0]
                self.sprite = self.obsticle[1][random.randint(0,5)]
                self.sprite = pygame.transform.scale_by(self.sprite, self.scaleFactor)
            else:
                self.obsticle = OBSTICLES[1]
                self.sprite = self.obsticle[1][0]
                self.y = self.y - LEVELS_OF_FLIGHT[random.randint(0,2)]
                self.sprite = pygame.transform.scale_by(self.sprite, 1)
            
            self.rect_coords = [self.sprite.get_width(), self.sprite.get_height()]
            self.x = GAME_WIDTH

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y-self.sprite.get_height()))

        if HIT_BOXES: pygame.draw.rect(screen, "red", self.rect, 2)

    def collide(self, dino):
        if self.rect.colliderect(dino.rect):
            lost.play()
            return True