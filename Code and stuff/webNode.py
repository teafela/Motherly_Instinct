import pygame, math, sys, random, os
from utilities import *
from globals import *

MAX_WEB_DENSITY = 80.0
NEARBY_NODE_DISTANCE = 200


class WebNode(object):

    id = 0
    img = 0
    
    def __init__(self, x, y, other_webNodes, connections):
        
        if WebNode.img == 0:
            WebNode.img = pygame.image.load(resource_path('web_node.png')).convert_alpha()
    
        self.img_rect = WebNode.img.get_rect()
        
        self.w = self.img_rect.width
        self.h = self.img_rect.height
        
        self.img_rect = pygame.Rect(x-self.w/2.0, y-self.h/2.0, self.w, self.h)
        
        self.id = WebNode.id
        WebNode.id += 1
        
        self.pos = Vector2D(x,y) # center
        
        for webNode in other_webNodes:
            if self.pos.distance(webNode.pos) < NEARBY_NODE_DISTANCE:
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
        
        self.create_point_list()
        
        
    def create_point_list(self):
        # build a list of Vector2D points going from webNode1 to webNode2
        self.point_list = []
        
        A = (self.webNode1.pos.x, self.webNode1.pos.y)
        C = (self.webNode2.pos.x, self.webNode2.pos.y)
        
        B = ( (A[0] + C[0])/2.0, (A[1] + C[1])/2.0 )
        B = ( (B[0] + GAME_WIDTH/2.0)/2.0, (B[1] + GAME_HEIGHT/2.0)/2.0 ) # TODO: weighted average and constants
        
        last_pos = bezier(A, B, C, 0)
        self.point_list.append(Vector2D(last_pos[0], last_pos[1]))
        
        # closer -> less web_density
        web_density = MAX_WEB_DENSITY - ( 1 - self.webNode1.pos.distance(self.webNode2.pos)/NEARBY_NODE_DISTANCE  ) * MAX_WEB_DENSITY
        # further from center -> more web_density
        
        # print "web_density before:", web_density
        
        if web_density <= 40:
            web_density += Vector2D( (A[0] + C[0])/2.0, (A[1] + C[1])/2.0 ).distance(Vector2D(GAME_WIDTH/2.0, GAME_HEIGHT/2.0)) / 15.0
        
        print "web_density after:", web_density
        if web_density >= 0.1:
            for t in [ i / web_density for i in range(int(web_density+2)) ]:
                current_pos = bezier(A, B, C, t)
                last_pos = current_pos
                self.point_list.append(Vector2D(last_pos[0], last_pos[1]))
        
    def includes(self, webNode):
        return self.webNode1 == webNode or self.webNode2 == webNode
        
    def includes_both(self, webNode1, webNode2):
        return (self.webNode1 == webNode1 and self.webNode2 == webNode2) or (self.webNode1 == webNode2 and self.webNode2 == webNode1)
        
    def point_close_to(self, point):
        return point.distance(self.webNode1.pos) < NEARBY_NODE_DISTANCE/2.0 or point.distance(self.webNode2.pos) < NEARBY_NODE_DISTANCE/2.0
        
    def print_connection(self):
        print "Node #", self.webNode1.id, "is connected to Node #", self.webNode2.id
        
    def draw(self, screen):
        max = len(self.point_list)
        
        for i in range(1,max):
            pygame.draw.aaline(screen, (240,240,240), (self.point_list[i-1].x, self.point_list[i-1].y), (self.point_list[i].x, self.point_list[i].y), 1 )
    
        # pygame.draw.aaline(screen, (240,240,240), (self.webNode1.pos.x, self.webNode1.pos.y), (self.webNode2.pos.x, self.webNode2.pos.y), 1 )
        # pygame.draw.aaline(screen, (200,200,200), (self.webNode1.pos.x+1, self.webNode1.pos.y+1), (self.webNode2.pos.x, self.webNode2.pos.y+1), 1 )
        
        