import pygame
from page import MainMenu
from globals import GAME_WIDTH, GAME_HEIGHT, SOUNDS

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Dino Game")
        self.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        self.clock = pygame.time.Clock()

        self.running = True
        self.current_page = MainMenu(self)

        with open("options.txt", "r") as f:
            options = f.readlines()
            volume = float(options[0].split(' ')[1].replace('\n', ''))
            for sound in SOUNDS:
                pygame.mixer.Sound.set_volume(sound, volume/100)
            

    def switch_page(self, new_page_class):
        
        self.current_page = new_page_class(self)

    def run(self):
        while self.running:
            self.current_page.run()

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
