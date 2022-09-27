from telnetlib import GA
import pygame
from pygame.locals import *
from battlefield import Battlefield
from text import Text

class Game:
    """Single-window with multiple scenes."""

    def __init__(self):
        pygame.init()
        flags = RESIZABLE

        
        Game.caption = "Battlecity: menu"
        pygame.display.set_caption(Game.caption)
        Game.clock = pygame.time.Clock()
        Game.screen = pygame.display.set_mode((1280, 1024), flags)
        Game.running = True

        self.render_menu()

        Game.keys_dict = {
            K_s: "print('Key press S')",
            K_g: "Battlefield(Game.screen).run()"
        }
    
    def render_menu(self):
        Game.image = pygame.image.load(r'images\skinner.png')
        Game.image.convert()

    def run(self):
        """Main event loop."""
        while Game.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    Game.running = False
                if event.type == KEYDOWN:
                    if event.key in Game.keys_dict:
                        self.do_shortcut(event)
                        pygame.display.set_caption(Game.caption)

                Game.screen.blit(Game.image, Game.screen.get_rect())
                self.type_go_text()
                pygame.display.update()
                Game.clock.tick(30)

        pygame.quit()

    def type_go_text(self):
        central_text = "Press 'g' to go on Battlefield"
        text = Text(central_text, (640, 512), fontsize=64, color='white')
        text.draw(Game.screen)

    def do_shortcut(self, event):
        """Execute combination"""
        k = event.key

        if k in Game.keys_dict:
            exec(Game.keys_dict[k])

if __name__ == '__main__':
    Game().run()