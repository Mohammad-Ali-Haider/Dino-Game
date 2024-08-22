import pygame
from globals import FONT, GAME_WIDTH, SPEED, SOUNDS, points
from scores import save_score, load_score
from ground import Ground
from obsticle import Obsticle
from dino import Dino

class Page:
    def __init__(self, game) -> None:
        self.game = game
        self.screen = game.screen

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
                self.running = False

    def update(self):
        pass

    def render(self):
        pass

    def run(self):
        self.handle_events()
        self.update()
        self.render()
        pygame.display.flip()


class MainMenu(Page):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.Font(None, 74)
        self.options_font = pygame.font.Font(None, 36)

        self.options = ["Start Game", "Settings", "Exit"]
        self.selected_option = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0:
                        self.game.switch_page(Gameplay)
                    elif self.selected_option == 1:
                        self.game.switch_page(Settings)
                    elif self.selected_option == 2:
                        self.game.running = False
                        self.running = False

    def update(self):
        pass

    def render(self):
        self.screen.fill((30, 30, 30))
        title_surface = self.title_font.render("Dino Game", True, (255, 255, 255))
        self.screen.blit(title_surface, (self.screen.get_width() // 2 - title_surface.get_width() // 2, 50))

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (150, 150, 150)
            option_surface = self.options_font.render(option, True, color)
            self.screen.blit(option_surface, (self.screen.get_width() // 2 - option_surface.get_width() // 2, 150 + i * 40))

    def run(self):
        self.handle_events()
        self.update()
        self.render()
        pygame.display.flip()


class Gameplay(Page):
    def __init__(self, game):
        super().__init__(game)
        self.base_speed = SPEED
        self.speed_multiplier = 1.0
        self.high_score = load_score() | 1

        self.movement = True
        self.score = 1

        self.dino = Dino()
        self.grounds = [Ground(0), Ground(624*3)]
        self.obsticles = [Obsticle(GAME_WIDTH)]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.switch_page(MainMenu)
        
        self.key_presses()
                
        super().handle_events()

    def key_presses(self):
        keys = pygame.key.get_pressed()
        if self.movement:
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.dino.jump()
            if keys[pygame.K_DOWN]: 
                if self.dino.isGrounded: self.dino.duck()
                else: self.dino.smash_down()
            else: self.dino.reset_collider()
        else:
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.score = 1
                self.movement = True
                self.dino.reset()
                self.obsticles.clear()
                self.obsticles.append(Obsticle(700))

    def update(self, dt):
        if self.movement:
            for ground in self.grounds:
                ground.move(self.base_speed * self.speed_multiplier)
            for obsticle in self.obsticles:
                obsticle.move(self.base_speed * self.speed_multiplier)

            self.score += 0.1
            if int(self.score) % 100 == 0:
                self.score += 1
                points.play()

            self.speed_multiplier = 1.0 + self.score / 1000

            for ground in self.grounds:
                if ground.collide(self.dino): self.dino.isGrounded = True
                self.dino.move(dt)

            for obsticle in self.obsticles:
                if obsticle.collide(self.dino):
                    if self.score > self.high_score:
                        self.high_score = int(self.score)
                        save_score(self.high_score)
                    self.movement = False

    def render(self):
        self.screen.fill("white")
        score_text = FONT.render(f"Score: {int(self.score)}", True, (102, 102, 102), (255, 255, 255))
        self.screen.blit(score_text, (20, 50))
        high_score_text = FONT.render(f"High Score: {self.high_score}", True, (102, 102, 102), (255, 255, 255))
        self.screen.blit(high_score_text, (20, 20))
        for ground in self.grounds:
            ground.draw(self.screen)
        for obsticle in self.obsticles:
            obsticle.draw(self.screen)
        self.dino.draw(self.screen)

    def run(self):
        dt = self.game.clock.tick(60)/ 1000
        self.handle_events()
        self.update(dt)
        self.render()
        pygame.display.flip()


class Settings(Page):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.Font(None, 74)
        self.options_font = pygame.font.Font(None, 36)
        with open("options.txt", "r") as f:
            options = f.readlines()
            self.volume = float(options[0].split(' ')[1].replace('\n', ''))
        self.options = [f"Volume: {self.volume}", "Back"]
        self.selected_option = 0

    def handle_events(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 1:
                        for sound in SOUNDS:
                            pygame.mixer.Sound.set_volume(sound, self.volume/100)
                        with open("options.txt", "w") as f:
                            f.write(f"Volume: {self.volume}\n")
                        self.game.switch_page(MainMenu)
        keys = pygame.key.get_pressed()
        if self.selected_option == 0:
            if keys[pygame.K_RIGHT] and self.volume < 100:
                self.volume += int(100 * dt)
                self.options = [f"Volume: {self.volume}", "Back"]
            elif keys[pygame.K_LEFT] and self.volume > 0:
                self.volume -= int(100 * dt)
                self.options = [f"Volume: {self.volume}", "Back"]


    def run(self):
        dt = self.game.clock.tick(60)/1000
        self.handle_events(dt)
        self.update()
        self.render()
        pygame.display.flip()

    def update(self):
        pass

    def render(self):
        self.screen.fill((30, 30, 30))
        title_surface = self.title_font.render("Settings", True, (255, 255, 255))
        self.screen.blit(title_surface, (self.screen.get_width() // 2 - title_surface.get_width() // 2, 50))

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (150, 150, 150)
            option_surface = self.options_font.render(option, True, color)
            self.screen.blit(option_surface, (self.screen.get_width() // 2 - option_surface.get_width() // 2, 150 + i * 40))
