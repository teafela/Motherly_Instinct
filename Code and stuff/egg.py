import pygame, math, sys, random, os
from utilities import *
from globals import *

class Egg(object):
    
    id = 0
    img = 0
    
    def __init__(self):
        
        self.id = Egg.id
        Egg.id += 1
        
        if Egg.img == 0:
            Egg.img = pygame.image.load(resource_path('eggs.png')).convert_alpha()
        self.img_rect = Egg.img.get_rect()
        
        self.w = self.img_rect.width
        self.h = self.img_rect.height
        
        self.pos = self.choosePosition()
        
        self.img_rect = pygame.Rect(self.pos.x-self.w/2.0,self.pos.y-self.h/2.0,self.w, self.h)
    
    
    def choosePosition(self):
        #choses starting position (initializer helper)
        #change this if you want the position of the eggs to start out differently
        return Vector2D(GAME_WIDTH/2 + random.randint(-60, 60),GAME_HEIGHT/2 + random.randint(-60, 60))
    
    
    def update(self):
        pass
    
    
    def draw(self, screen):
        screen.blit(Egg.img, self.img_rect)