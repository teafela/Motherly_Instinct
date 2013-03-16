# ---------------------------------------------------------------------------------------
# Game Jam 10/27/2012 - 10/28/2012
#   Motherly Instinct
#   Brian Tam, Ronald Sardarian, Scott Todd
# ---------------------------------------------------------------------------------------

import pygame, math, sys, random
from spider import *
from webNode import *
from enemy import *
from HUD import *

# ---------------------------------------------------------------------------------------    
# Game class, used to track essential game values and calls other logic
        
class Game(object):
    def __init__(self):
        # self.screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.game_screen = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.game_over = False
        self.game_exit = False
        self.clock = pygame.time.Clock()
        
        self.game_bg = pygame.image.load("resources/game-bg.png").convert_alpha()
        self.hud_bg = pygame.image.load("resources/HUD/hud-bg.png").convert_alpha()

        self.player = Spider()
        
        self.webNode_list = []
        self.connection_list = []
        self.enemy_list = []
        self.egg_list = [] # len(self.egg_list) is your lives
        
        for i in range(0,8):
            self.egg_list.append(Egg())
        
        self.time_until_spawn = 20000 # milliseconds
        self.spawn_wait_start_time = pygame.time.get_ticks()
        self.total_enemies_this_wave = random.randint(4,6)
        self.enemies_spawned_this_wave = 0
        
        self.timer = 20
        self.timer_past_time = pygame.time.get_ticks()
        
        self.wave_number = 0    
        
        self.node_delay = 500
        self.node_prev_ticks = 0
        
        self.venom_delay = 200
        self.venom_prev_ticks = 0
        
        self.score = 0
        self.last_score_time = pygame.time.get_ticks()
        
        self.HUD = HUD()
        
        self.sfx_attack = pygame.mixer.Sound("resources/Sounds/spiderling_cast_edited2.wav")
        self.sfx_web = pygame.mixer.Sound("resources/Sounds/web_cast_edited2.wav")
        self.sfx_egg_die = pygame.mixer.Sound("resources/Sounds/spiderling_impact_edited2.wav")
        
        # self.sfx_web_loop = pygame.mixer.Sound("resources/Sounds/web_loop.wav")
        # self.sfx_web_loop2 = pygame.mixer.Sound("resources/Sounds/web_loop.wav")
        # self.sfx_web_loop.set_volume(0.5)
        # self.sfx_web_loop.play(-1)
        # self.ambient_timer = pygame.time.get_ticks()
        # self.ambient_playing = False
        
        
        
    def process_events(self):
        key = pygame.key.get_pressed() # all keys currently pressed, used for continued actions (movement)
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            self.player.move_left()
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.player.move_right()
        if key[pygame.K_UP] or key[pygame.K_w]:
            self.player.move_up()
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            self.player.move_down()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    self.game_exit = True
                if event.key == pygame.K_z:
                    if (pygame.time.get_ticks() - self.node_prev_ticks) > self.node_delay and self.player.web >= 100:
                        self.webNode_list.append(WebNode(self.player.pos.x, self.player.pos.y, self.webNode_list, self.connection_list))
                        self.player.web -= 100
                        self.node_prev_ticks = pygame.time.get_ticks()
                        self.sfx_web.play()
                        
                if event.key == pygame.K_x:
                    if (pygame.time.get_ticks() - self.venom_prev_ticks) > self.venom_delay and self.player.venom >= 167:
                        for enemy in self.enemy_list:
                            if enemy.pos.distance(self.player.pos) <= 30 and enemy.stoptime > 0:
                                # self.enemy_list.remove(enemy)
                                self.sfx_attack.play()
                                enemy.start_dying()
                                self.player.venom -= 167
                                self.player.attack()
                                self.venom_prev_ticks = pygame.time.get_ticks()
                                if not self.game_over:
                                    self.score += 50
                                break
                    
                # if event.key == pygame.K_SPACE:
                    # self.delete_webNode( random.randint( 0, len(self.webNode_list) - 1 ))
                    # self.delete_webNode( 0 )
                # if event.key == pygame.K_p:
                    # for connection in self.connection_list:
                        # connection.print_connection()
                    # print ""
                    

                    
    def update(self):
        # if pygame.time.get_ticks() - self.ambient_timer > 5000 and not self.ambient_playing:
            # self.sfx_web_loop2.set_volume(0.5)
            # self.sfx_web_loop2.play(-1)
            # self.ambient_playing = True
    
        while pygame.time.get_ticks() - self.last_score_time > 1000:
            self.last_score_time += 1000
            if not self.game_over:
                self.score += 5
    
        if pygame.time.get_ticks() - self.spawn_wait_start_time > self.time_until_spawn:
            if random.random() < 0.02:
                self.enemy_list.append(Enemy())
                self.enemies_spawned_this_wave += 1
            if self.enemies_spawned_this_wave == self.total_enemies_this_wave:
                self.spawn_wait_start_time = pygame.time.get_ticks()
                self.total_enemies_this_wave += random.randint(1,3)
                self.enemies_spawned_this_wave = 0
                # Reset timer
                # self.timer = 20 + random.randint(-2*self.wave_number,2*self.wave_number)
                self.timer_past_time = pygame.time.get_ticks()
                
                self.time_until_spawn = random.randint(18000-1000*self.wave_number, 22000+1000*self.wave_number)
                self.timer = self.time_until_spawn / 1000 + random.randint(-3*self.wave_number,3*self.wave_number)
                if self.timer < 0:
                    self.timer = 0
                
                # print "time_until_spawn:", self.time_until_spawn
                # print "timer:", self.timer
                
                
                self.wave_number += 1
                
        if pygame.time.get_ticks() - self.timer_past_time > 1000:
            if self.timer > 0:
                self.timer -= 1
            self.timer_past_time = pygame.time.get_ticks()
    
        self.player.update()
    
        for webNode in self.webNode_list:
            webNode.update()
            
        for egg in self.egg_list:
            egg.update()
            
        for enemy in self.enemy_list:
            enemy.update(self.enemy_list, self.connection_list)
            
            # check for breaking loose from a web and destroy a node
            if enemy.broke_loose():
                which_to_delete = random.randint(1,2)
                i = 0
                for webNode in self.webNode_list:
                    if webNode == enemy.stuckTo.webNode1 and which_to_delete == 1:
                        self.delete_webNode(i)
                    if webNode == enemy.stuckTo.webNode2 and which_to_delete == 2:
                        self.delete_webNode(i)
                    i += 1
            
            # check for reaching the center and destroy an egg
            if enemy.reached_center():
                if len(self.egg_list) > 0:
                    self.sfx_egg_die.play()
                    self.egg_list.pop()
                
        # remove enemys that reached the center from the list and enemies that died
        self.enemy_list[:] = [enemy for enemy in self.enemy_list if not enemy.reached_center() and not enemy.is_dead]
        
        if len(self.egg_list) == 0:
            self.game_over = True
        
    def delete_webNode(self, webNode_list_index):
        webNode = self.webNode_list[webNode_list_index]
        
        webNode.delete_all_connections(self.connection_list)
        self.webNode_list.pop(webNode_list_index)
        
        for enemy in self.enemy_list:
            if not enemy.stuckTo in self.connection_list:
                enemy.break_loose()
        
    def draw(self):
        self.screen.fill((30,30,30))
        self.game_screen.fill((80,80,80))
        self.screen.blit( self.hud_bg, pygame.Rect(768, 0, self.hud_bg.get_width(), self.hud_bg.get_height()))
        self.game_screen.blit( self.game_bg, pygame.Rect(0, 0, self.game_bg.get_width(), self.game_bg.get_height()))
        
        for connection in self.connection_list:
            connection.draw(self.game_screen)
        
        for webNode in self.webNode_list:
            webNode.draw(self.game_screen)
        
        for egg in self.egg_list:
            egg.draw(self.game_screen)
        
        for enemy in self.enemy_list:
            enemy.draw(self.game_screen)
        
        # redraw the player object (above all other objects)
        self.player.draw(self.game_screen)
        
        # HUD
        self.HUD.draw(self.screen, self.player, self.timer, len(self.egg_list), self.score, self.game_over)
        
        self.screen.blit(self.game_screen, (0, 0))
        

        
        
# ---------------------------------------------------------------------------------------    


# ---------------------------------------------------------------------------------------    
# Overall game logic. Creates a Game object and calls its functions in order, draws to the screen

pygame.init()
pygame.display.set_caption("Motherly Instinct")
g = Game()
pygame.key.set_repeat()

while not g.game_exit:
    g.clock.tick(30)
    g.process_events()
    g.update()
    g.draw()
    pygame.display.flip()

    
sys.exit()
    
    
    
    
    
    
