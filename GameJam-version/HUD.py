import pygame
from time import localtime, strftime, time
from operator import attrgetter
from utilities import *

class HUD(object):

    def __init__(self):
        self.web_base = pygame.image.load("resources/HUD/web-base.png").convert_alpha()
        self.web_rect = pygame.Rect(857,100,self.web_base.get_width(),self.web_base.get_height())
        self.web_fill = pygame.image.load("resources/HUD/web-fill.png").convert_alpha()
        
        self.venom_base = pygame.image.load("resources/HUD/venom-base.png").convert_alpha()
        self.venom_rect = pygame.Rect(911,100,self.venom_base.get_width(),self.venom_base.get_height())
        self.venom_fill = pygame.image.load("resources/HUD/venom-fill.png").convert_alpha()
        
        self.egg = pygame.image.load("resources/eggs.png").convert_alpha()
        
        self.font = pygame.font.Font("resources/HUD/Spiderfingers.ttf", 42)
        self.font_small = pygame.font.Font("resources/HUD/Spiderfingers.ttf", 24)
        
        self.initials = [0, 0, 0]
        self.initials_index = 0
    
    
    def draw(self, screen, player, timer, eggs, score, game_over):
        # Timer
        timer_text = str(timer).zfill(2)
        for i in range(0, len(timer_text)):
            digit = timer / (10**(len(timer_text)-1-i)) % 10
            txt = self.font.render(str(digit), True, (200,200,200))
            screen.blit(txt, pygame.Rect( 877 + 24*i, 25, 100, 42))
        
        # Web bar
        web_height = (player.web) / 2.0
        web_bar_section = pygame.Rect(0,web_height-self.web_rect.height, self.web_rect.width, self.web_rect.height)
        screen.blit( self.web_fill, self.web_rect, web_bar_section)
        screen.blit( self.web_base,  self.web_rect)
        
        # Venom Bar
        venom_height = (player.venom) / 2.0
        venom_bar_section = pygame.Rect(0,venom_height-self.venom_rect.height, self.venom_rect.width, self.venom_rect.height)
        screen.blit( self.venom_fill, self.venom_rect, venom_bar_section)
        screen.blit( self.venom_base,  self.venom_rect)
        
        # Eggs
        for i in range(0,eggs):
            #                                                   350 is bottom of bars
            screen.blit( self.egg, pygame.Rect( 852 + 22*(i%4), 400 + 22*(i/4), self.egg.get_width(), self.egg.get_height()))
            
        # Score
        score_text = str(score).zfill(5)
        for i in range(0, len(score_text)):
            digit = score / (10**(len(score_text)-1-i)) % 10
            txt = self.font.render(str(digit), True, (200,200,200))
            screen.blit(txt, pygame.Rect( 840 + 24*i, 494+26, 100, 42))
            
        # Static text
        x = 785
        y = 18
        txt = self.font_small.render("Time to", True, (200,200,200))
        screen.blit(txt, pygame.Rect( x, y, 100, 42))
        txt = self.font_small.render("next wave:", True, (200,200,200))
        screen.blit(txt, pygame.Rect( x, y+26, 100, 42))
        
        txt = self.font_small.render("Score", True, (200,200,200))
        x = 876 # 768+(128 - txt.get_width()/2)
        screen.blit(txt, pygame.Rect( x, 494, 100, 42))
        
        # Game Over
        if game_over:
            x = 832
            y = 670
            txt = self.font.render("GAME OVER", True, (172,0,0))
            screen.blit(txt, pygame.Rect( x, y, 100, 42))

        
    
    
    
    