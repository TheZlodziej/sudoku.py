import pygame
from consts import *

class Tile:
    def __init__(self, x, y, value=0, filled=False): #change default value to blank tekst
        self.w = TILE_SIZE[0]
        self.h = TILE_SIZE[1]
        self.x = x
        self.y = y
        self.rect = (x,y,TILE_SIZE[0], TILE_SIZE[1])
        self.value = value
        self.color = TILE_COLOR
        self.filled = filled
        self.selected = False
    
    def draw(self, window):
        if self.filled and not self.selected:
            self.color = FILLED_TILE_COLOR
        pygame.draw.rect(window, self.color, self.rect)
        if self.value > 0:
            text=pygame.font.SysFont(pygame.font.get_default_font(), FONT_SIZE).render(str(self.value), True, TEXT_COLOR)
            window.blit(text, (self.x + self.w//2 - text.get_width()//2, self.y + self.h//2 - text.get_height()//2))