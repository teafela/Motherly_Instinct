import pygame, math, sys, random, os
from utilities import *
from globals import *

MOVE_SPEED = 2.75
SPEED_DAMPENING = 0.55

class Spider(object):
    
    def __init__(self, game_time):
        
        self.img = pygame.image.load(resource_path('spider.png')).convert_alpha()
        self.img_rect = self.img.get_rect()
        
        #self.w = self.img_rect.width
        #self.h = self.img_rect.height
        
        self.pos = Vector2D(GAME_WIDTH/2.0, GAME_HEIGHT/2.0) # center
        self.vel = Vector2D()
        
        self.recharge_time = game_time
        self.web = 500 # Max
        self.venom = 0
        
        self.update_speed = 75
        self.frame = 0
        self.frame_start_time = game_time
        
        self.direction = 0
        self.pose = 0
        self.pose_height = 356              # 356 px height for each pose
        self.w = self.img_rect.width / 4    # 4 Col
        self.h = self.img_rect.height / 8   # 8 Row
        self.source = pygame.Rect(self.frame*self.w,self.direction*self.h + self.pose * self.pose_height ,self.w,self.h)
       
       
    def move_right(self):
        self.vel.x += MOVE_SPEED
    
    def move_left(self):
        self.vel.x -= MOVE_SPEED
        
    def move_up(self):
        self.vel.y -= MOVE_SPEED
        
    def move_down(self):
        self.vel.y += MOVE_SPEED
        
    def get_direction(self):
        if abs(self.vel.x) > abs(self.vel.y):
            # Right
            self.direction = 1
            # Left
            if self.vel.x < 0:
                self.direction = 2
        else:
            # Down
            self.direction = 0
            if self.vel.y < 0:
                self.direction = 3
                
    def attack(self):
        self.frame = 0
        self.pose = 1
        
    def update(self, game_time):
        
        self.get_direction()
        
        while game_time - self.frame_start_time > self.update_speed:
            self.frame_start_time += self.update_speed
            if (self.vel.magnitude() > 1 or self.pose == 1):
                self.frame = (self.frame + 1) % 4
        self.source = pygame.Rect(self.frame*self.w,self.direction*self.h + self.pose * self.pose_height ,self.w,self.h)
        
        # Walking pose idle reset
        if self.pose == 0 and self.vel.magnitude() < 1:
            self.frame = 0
        
        # Attack pose reset
        if self.pose == 1 and self.frame == 3:
            self.pose = 0
            self.frame = 0
        
        # self.vel.limit_magnitude(10)
        
        self.pos.add(self.vel)
        self.vel.mult(SPEED_DAMPENING)
        
        self.pos.limit_x_range(0,GAME_WIDTH)
        self.pos.limit_y_range(0,GAME_HEIGHT)
        
        self.img_rect = pygame.Rect(self.pos.x-self.w/2.0,self.pos.y-self.h/2.0,self.w, self.h)
        
        if game_time - self.recharge_time > 30:
            self.recharge_time = game_time
            if self.web < 500:  # Height of bar * refresh rate (250 * 2)
                self.web += 1
            if self.venom < 500:
                self.venom += 1
        
    def draw(self, screen):
        # screen.blit(self.img, self.img_rect, pygame.Rect(self.frame*32,32*self.move_state,32,32))
        screen.blit(self.img, self.img_rect, self.source)
        


        
        