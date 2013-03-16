import pygame, math, sys, random
from utilities import *

class WebNode(object):

    id = 0
    img = 0
    
    def __init__(self, x, y, other_webNodes, connections):
        
        if WebNode.img == 0:
            WebNode.img = pygame.image.load("resources/cookie.png").convert_alpha()
    
        self.img_rect = WebNode.img.get_rect()
        
        self.w = self.img_rect.width
        self.h = self.img_rect.height
        
        self.img_rect = pygame.Rect(x-self.w/2.0, y-self.h/2.0, self.w, self.h)
        
        self.id = WebNode.id
        WebNode.id += 1
        
        self.pos = Vector2D(x,y) # center
        
        for webNode in other_webNodes:
            if self.pos.distance(webNode.pos) < 200:
                self.add_connection(webNode, connections)
        
    def __eq__(self, other):
        return self.id == other.id
        
    def update(self):
        pass
        
    def add_connection(self, other, connections):
        already_connected = False
                
        for connection in connections:
            if connection.includes_both(self, other):
                already_connected = True
                
        if not already_connected:
            connections.append(WebNodeConnection(self, other))
            
    def delete_connection(self, other, connections):
        connections[:] = [connection for connection in connections if not connection.includes_both(self, other)]
        
    def delete_all_connections(self, connections):
        connections[:] = [connection for connection in connections if not connection.includes(self)]
        
    def draw(self, screen):
        # screen.blit(self.img, self.img_rect, pygame.Rect(self.frame*32,32*self.move_state,32,32))
        screen.blit(WebNode.img, self.img_rect)
           
class WebNodeConnection(object):
    
    def __init__(self, webNode1, webNode2):
        self.webNode1 = webNode1
        self.webNode2 = webNode2
        
        # build a list of Vector2D points going from webNode1 to webNode2
        self.point_list = []
        
        pos = Vector2D(self.webNode1.pos.x, self.webNode1.pos.y)
        vel = pos.subtract(self.webNode2.pos)
        vel.mult(-1/10.0)
        
        for i in range(0,10):
           self.point_list.append(Vector2D(pos.x, pos.y))
           pos.add(vel)
        
    def includes(self, webNode):
        return self.webNode1 == webNode or self.webNode2 == webNode
        
    def includes_both(self, webNode1, webNode2):
        return (self.webNode1 == webNode1 and self.webNode2 == webNode2) or (self.webNode1 == webNode2 and self.webNode2 == webNode1)
        
    def point_close_to(self, point):
        return point.distance(self.webNode1.pos) < 100 or point.distance(self.webNode2.pos) < 100
        
    def print_connection(self):
        print "Node #", self.webNode1.id, "is connected to Node #", self.webNode2.id
        
    def draw(self, screen):
        pygame.draw.aaline(screen, (240,240,240), (self.webNode1.pos.x, self.webNode1.pos.y), (self.webNode2.pos.x, self.webNode2.pos.y), 1 )
        pygame.draw.aaline(screen, (200,200,200), (self.webNode1.pos.x+1, self.webNode1.pos.y+1), (self.webNode2.pos.x, self.webNode2.pos.y+1), 1 )
        