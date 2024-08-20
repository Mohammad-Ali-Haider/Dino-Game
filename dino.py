import pygame
from globals import HIT_BOXES, JUMP_VEL, GRAVITY, jump

class Dino:

    def __init__(self) -> None:
        self.x = 100
        self.y = 325
        self.velocity = 0
        self.frame = 0
        self.isDuck = False
        self.isGrounded = False
        self.sprites = [pygame.image.load(f"assets/Dino1.png"),pygame.image.load(f"assets/Dino2.png"),pygame.image.load(f"assets/DinoJumping.png"),pygame.image.load(f"assets/DinoDucking1.png"),pygame.image.load(f"assets/DinoDucking2.png")]
        self.rect = pygame.Rect((self.x, self.y), (self.sprites[0].get_width(), self.sprites[0].get_height()))

    def draw(self, screen):
        self.screen = screen or None
        if int(self.frame) >= 2: self.frame = 0
        if self.isDuck:
            if int(self.frame) == 0: screen.blit(self.sprites[3], (self.x, self.y+self.sprites[0].get_height()/2-10))
            if int(self.frame) == 1: screen.blit(self.sprites[4], (self.x, self.y+self.sprites[0].get_height()/2-10))
        elif self.isGrounded:
            if int(self.frame) == 0: screen.blit(self.sprites[0], (self.x, self.y))
            elif int(self.frame) == 1: screen.blit(self.sprites[1], (self.x, self.y))
        else:
            screen.blit(self.sprites[2], (self.x, self.y))
        self.frame += 0.2
        if HIT_BOXES: pygame.draw.rect(screen, "green", self.rect, 2)

    def jump(self):
        if self.isGrounded:
            jump.play()
            self.isGrounded = False
            self.velocity = -JUMP_VEL

    def duck(self):
        self.rect = pygame.Rect((self.x, self.y+self.sprites[0].get_height()/2-10), (self.sprites[0].get_width()+10, self.sprites[0].get_height()/2+10))
        self.isDuck = True

    def smash_down(self):
        self.velocity = 1000

    def reset_collider(self):
        self.rect = pygame.Rect((self.x, self.y), (self.sprites[0].get_width(), self.sprites[0].get_height()))
        self.isDuck = False

    def move(self, dt):
        if not self.isGrounded or self.velocity<0:
            s = self.velocity * dt + 0.5 * GRAVITY * dt**2
            self.velocity += GRAVITY/1000
            self.y += s
            if self.y > 329: self.y = 329
            if self.y < 329: self.isGrounded = False
            self.rect = pygame.Rect((self.x, self.y), (self.sprites[0].get_width(), self.sprites[0].get_height()))
        
    def reset(self):
        self.x = 100
        self.y = 325