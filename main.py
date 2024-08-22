import pygame
import random

from scores import save_score, load_score

from dino import Dino
from obsticle import Obsticle
from ground import Ground
from globals import GAME_WIDTH, GAME_HEIGHT, SPEED, FONT, points

class App:

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode([GAME_WIDTH, GAME_HEIGHT])
        self.clock = pygame.time.Clock()
        self.base_speed = SPEED
        self.speed_multiplier = 1.0

    def draw(self, dino, grounds, obsticles, score):
        self.screen.fill("white")
        score_text = FONT.render(f"Score: {str(int(score))}", True, (102, 102, 102), (255, 255, 255))
        self.screen.blit(score_text, (20, 50))
        high_score_text = FONT.render(f"High Score: {str(load_score())}", True, (102, 102, 102), (255, 255, 255))
        self.screen.blit(high_score_text, (20, 20))
        for ground in grounds:
                ground.draw(self.screen)
                ground.move(self.base_speed * self.speed_multiplier)
        for obsticle in obsticles:
                obsticle.draw(self.screen)
                obsticle.move(self.base_speed * self.speed_multiplier)
        dino.draw(self.screen)
        pygame.display.flip()

    def run(self):
        running = True
        movement = True
        score = 0
        high_score = load_score()

        dino = Dino()
        grounds = [Ground(0), Ground(624*3)]
        obsticles = [Obsticle(GAME_WIDTH)]

        while running:
            [exit() for event in pygame.event.get() if event.type == pygame.QUIT]
            dt = self.clock.tick(60)/ 1000

            keys = pygame.key.get_pressed()

            if movement == True:
                score += 0.1
                if score % 100 == 0: points.play()

                self.speed_multiplier = 1.0 + score / 1000

                for ground in grounds:
                    if ground.collide(dino): dino.isGrounded = True
                    dino.move(dt)

                for obsticle in obsticles:
                    if obsticle.collide(dino): movement = False

                if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                    dino.jump()
                if keys[pygame.K_DOWN]: 
                    if dino.isGrounded: dino.duck()
                    else: dino.smash_down()
                else: dino.reset_collider()

                self.draw(dino, grounds, obsticles, score)
            else:
                if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                    if score > high_score: 
                        high_score = score
                        save_score(score)
                    score = 0
                    movement = True
                    dino.reset()
                    obsticles.clear()
                    obsticles = [Obsticle(700)]


if __name__ == "__main__":
    app = App()
    app.run()