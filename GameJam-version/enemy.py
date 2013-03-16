import pygame, math, sys, random
from utilities import *

MOVE_SPEED = 2.3
SPEED_DAMPENING = 0.75

class Enemy(object):
    
    img = 0
    
    def __init__(self):
        #image for enemy
        
        if Enemy.img == 0:
            Enemy.img = pygame.image.load("resources/ant.png").convert_alpha()
    
        # self.img = pygame.image.load("resources/orb.png").convert_alpha()
        # self.img_rect = pygame.Rect(0,0,32,32)
        self.img_rect = Enemy.img.get_rect()
        
        
        #change depending on grid size
        self.choosePosition(GAME_HEIGHT)
        
        #sets pos
        self.vel = Vector2D(2,2)
        self.acc = Vector2D()
        self.stoptime = 0
        self.stuckTo = 0
        
        self.update_speed = 75
        self.pose = 0
        self.is_dead = False
        self.frame = 4
        self.frame_start_time = pygame.time.get_ticks()
        self.direction = 0
        
        self.pose_height = 100
        self.w = self.img_rect.width / 4
        self.h = self.img_rect.height / 8
        self.source = pygame.Rect(self.frame*self.w,self.direction*self.h + self.pose * self.pose_height ,self.w,self.h)
        
        self.center_goal = Vector2D(GAME_WIDTH/2, GAME_HEIGHT/2)
        self.goalLocation = Vector2D(random.randint(0,GAME_WIDTH), random.randint(0,GAME_HEIGHT))
        self.wander_start_time = pygame.time.get_ticks()
        self.wander_time = random.randint(500,7000)
        
    def choosePosition(self, gridSize):
        #choses starting position (initializer helper)
        start = random.randint(0, gridSize)
        direction = random.randint(0, 3)
        if direction == 0 :
            self.pos = Vector2D(start ,0)
        elif direction == 1:
            self.pos = Vector2D(0, start)
        elif direction == 2:
            self.pos = Vector2D(start, GAME_HEIGHT)
        else:
            self.pos = Vector2D(GAME_WIDTH, start)
            
    def start_dying(self):
        self.pose = 1
        self.frame = 0
        
    # def is_dead(self):
        # return self.is_dead
        
    def accelerationToGoal(self):
        total = 0
        number = 0
        returned_vector = Vector2D()
        
        dX = (self.pos.x - self.goalLocation.x)
        dY = (self.pos.y - self.goalLocation.y)
        
        d = math.sqrt(dX*dX + dY*dY)
        
        returned_vector = Vector2D(-dX, -dY)
        if (d > 0):
            returned_vector.mult(80000/(d*d)) # further away = less influence, this is similar to gravity
            # print "to goal:", returned_vector.magnitude()
            
        returned_vector.limit_magnitude(30)
            
        return returned_vector
        
    def accerationAwayFromOthers(self, others):
        returned_vector = Vector2D()
        
        for other in others:
            if self.pos.distance(other.pos) < 300:
                dX = (self.pos.x - other.pos.x)
                dY = (self.pos.y - other.pos.y)
            
                added_vector = Vector2D(dX, dY)
                added_vector.mult(0.5)
                returned_vector.add(added_vector)
                
                
        # print "from others:", returned_vector.magnitude()
                
        returned_vector.limit_magnitude(20)
                
        return returned_vector
       
    def checkWebCollision(self, connectionList):
        for connection in connectionList:
            if connection.point_close_to(self.pos):
                for point in connection.point_list:
                    if self.pos.distance(point) < 10:
                        self.stuckTo = connection
                        self.stoptime = random.randint(80, 300)
                        
    def break_loose(self):
        self.stoptime = 0
        
        if random.random() < 0.5:
            self.goalLocation = Vector2D(random.randint(0,GAME_WIDTH), random.randint(0,GAME_HEIGHT))
            self.wander_start_time = pygame.time.get_ticks()
            self.wander_time = random.randint(500,7000)
      
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
            
    def update(self, enemies, connectionList):
    
        self.get_direction()
    
        if pygame.time.get_ticks() - self.frame_start_time > self.update_speed:
            self.frame = (self.frame + 1) % 4
            self.frame_start_time = pygame.time.get_ticks()
            if self.frame == 0 and self.pose == 1:
                self.is_dead = True
        self.source = pygame.Rect(self.frame*self.w,self.direction*self.h + self.pose * self.pose_height ,self.w,self.h)
        
        # self.vel.limit_magnitude(10)
        
        if self.stoptime <=0:
            self.checkWebCollision(connectionList)
            if self.stoptime <= 0:
                # self.vel = Vector2D()
                self.acc = Vector2D()
                
                if pygame.time.get_ticks() - self.wander_start_time > self.wander_time or self.pos.distance(self.goalLocation) < 10:
                    self.goalLocation = Vector2D(self.center_goal.x, self.center_goal.y)
                
                acc_to_goal = self.accelerationToGoal()
                acc_from_others = self.accerationAwayFromOthers(enemies)
                
                self.acc.add(acc_to_goal)
                self.acc.add(acc_from_others)
                self.acc.limit_magnitude(10)
                
                if self.pose == 0:
                    self.vel.add(self.acc)
                    self.vel.limit_magnitude(2)
            
            # self.setMove(enemies, 50)
        else:
            # self.vel = Vector2D(0,0)
            if self.vel.magnitude() > 0.005:
                self.vel.mult(1/10000.0)
            self.acc = Vector2D(0,0)
        self.pos.add(self.vel)
        self.stoptime -= 1
        # self.vel.mult(SPEED_DAMPENING)
        
        self.pos.limit_x_range(0,GAME_WIDTH)
        self.pos.limit_y_range(0,GAME_HEIGHT)
        
        self.img_rect = pygame.Rect(self.pos.x-self.w/2.0,self.pos.y-self.h/2.0,self.w, self.h)
        
    def broke_loose(self):
        return self.stoptime == 0
    
    def reached_center(self):
        return self.pos.distance(self.center_goal) < 3
        
    def draw(self, screen):
        # screen.blit(self.img, self.img_rect, pygame.Rect(self.frame*32,32*self.move_state,32,32))
        screen.blit(Enemy.img, self.img_rect, self.source)
        
