# ---------------------------------------------------------------------------------------
# Game Jam 10/27/2012 - 10/28/2012
#   Motherly Instinct
#   Brian Tam, Ronald Sardarian, Scott Todd
#   Made under the themes of Surprise and Suspense.
# ---------------------------------------------------------------------------------------

import pygame, math, sys, random, os
from spider import *
from webNode import *
from egg import *
from enemy import *
from HUD import *
from globals import *
from utilities import *

# ---------------------------------------------------------------------------------------    
# Game class, used to track essential game values and calls other logic

ARCADE_CABINET = False
DEBUG_MODE = False

class Game(object):
    def __init__(self):
        # self.screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.game_screen = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.game_over = False
        self.game_exit = False
        self.clock = pygame.time.Clock()
        
        if ARCADE_CABINET:
            self.KEYS = {
                'left': [pygame.K_a], 
                'right': [pygame.K_d], 
                'up': [pygame.K_w], 
                'down': [pygame.K_d], 
                'quit': [pygame.K_f], 
                'web': [pygame.K_z], 
                'attack': [pygame.K_x], 
                'restart': [pygame.K_3], 
                'pause': [pygame.K_5], 
                'confirm': [pygame.K_c], 
                'suicide': [pygame.K_v]
            }
            
        if not ARCADE_CABINET:
            self.KEYS = {
                'left': [pygame.K_LEFT, pygame.K_a], 
                'right': [pygame.K_RIGHT, pygame.K_d], 
                'up': [pygame.K_UP, pygame.K_w], 
                'down': [pygame.K_DOWN, pygame.K_s], 
                'quit': [pygame.K_ESCAPE], 
                'web': [pygame.K_z, pygame.K_PERIOD], 
                'attack': [pygame.K_x, pygame.K_SLASH], 
                'restart': [pygame.K_r], 
                'pause': [pygame.K_p], 
                'confirm': [pygame.K_SPACE, pygame.K_RETURN], 
                'suicide': [pygame.K_v]
            }

        self.game_bg = pygame.image.load(resource_path('game-bg.png')).convert_alpha()
        self.hud_bg = pygame.image.load(resource_path(os.path.join('HUD', 'hud-bg.png'))).convert_alpha()
        
        self.pause_screen = pygame.image.load(resource_path('pause.png')).convert_alpha()
        
        self.game_time = pygame.time.get_ticks()
        self.paused = False
        self.pause_time = 0

        # Call initializing stff
        self.start_game()
        
        self.HUD = HUD()
        
        self.sfx_attack = pygame.mixer.Sound(resource_path(os.path.join('Sounds', 'spider attack (freesfx.co.uk).wav')))
        self.sfx_kill = pygame.mixer.Sound(resource_path(os.path.join('Sounds', 'spider kill (freesfx.co.uk).wav')))
        self.sfx_web = pygame.mixer.Sound(resource_path(os.path.join('Sounds', 'web (freesfx.co.uk).wav')))
        self.sfx_egg_die = pygame.mixer.Sound(resource_path(os.path.join('Sounds', 'egg die (freesfx.co.uk).wav')))
        
        self.sfx_ambient = pygame.mixer.Sound(resource_path(os.path.join('Sounds', 'ambient.wav')))
        # self.sfx_ambient.set_volume(0.3)
        self.sfx_ambient.play(-1)
        
        self.score_made = False
        
        
    def splash_screen(self):
        # Start of game splash screen
        splash = True
        
        if ARCADE_CABINET:
            splash_background = pygame.image.load(resource_path('instructions-arcade.png')).convert_alpha()
            
        if not ARCADE_CABINET:
            splash_background = pygame.image.load(resource_path('instructions-keyboard.png')).convert_alpha()
        
        splash_background_rect = splash_background.get_rect()
        self.screen.blit(splash_background, splash_background_rect)
        pygame.display.flip()
        
        all_movement_keys = []
        for key in self.KEYS['left']:
            all_movement_keys.append(key)
        for key in self.KEYS['right']:
            all_movement_keys.append(key)
        for key in self.KEYS['up']:
            all_movement_keys.append(key)
        for key in self.KEYS['down']:
            all_movement_keys.append(key)
            
        while (splash):
            self.pause_time = pygame.time.get_ticks() - self.game_time
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_exit = True
                    splash = False
                if event.type == pygame.KEYDOWN:
                    if not event.key in all_movement_keys:
                        splash = False
                    if event.key in self.KEYS['quit']:
                        self.game_exit = True
                        
        
    def start_game(self):
        self.splash_screen()
        self.paused = False
        self.player = Spider(self.game_time)
        
        self.webNode_list = []
        self.connection_list = []
        self.enemy_list = []
        self.egg_list = []
        
        for i in range(0,8):
            self.egg_list.append(Egg())
        
        self.time_until_spawn = 20000 # milliseconds
        self.spawn_wait_start_time = self.game_time
        self.total_enemies_this_wave = random.randint(4,6)
        self.enemies_spawned_this_wave = 0
        
        self.timer = 20
        self.timer_past_time = self.game_time
        
        self.wave_number = 0    
        
        self.node_delay = 500
        self.node_prev_ticks = 0
        
        self.venom_delay = 200
        self.venom_prev_ticks = 0
        
        self.score = 0
        self.last_score_time = self.game_time
        
        
    def process_events(self):
        if not self.paused:
            key = pygame.key.get_pressed() # all keys currently pressed, used for continued actions (movement)
            for test_key in self.KEYS['left']:
                if key[test_key]:
                    self.player.move_left()
                    break
                    
            for test_key in self.KEYS['right']:
                if key[test_key]:
                    self.player.move_right()
                    break
                    
            for test_key in self.KEYS['up']:
                if key[test_key]:
                    self.player.move_up()
                    break
                    
            for test_key in self.KEYS['down']:
                if key[test_key]:
                    self.player.move_down()
                    break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_exit = True
        
            if event.type == pygame.KEYDOWN: 
                if event.key in self.KEYS['quit']:
                    self.game_exit = True
                if event.key in self.KEYS['restart']:
                    if not (self.game_over and not self.score_made):    # Can restart whenever except during high score input.
                        self.reset_game()
                if event.key in self.KEYS['pause']:
                    self.paused = not self.paused
                if DEBUG_MODE:
                    if event.key in self.KEYS['suicide']:
                        self.game_over = True
                if not self.paused:
                    if event.key in self.KEYS['web']:
                        if (self.game_time - self.node_prev_ticks) > self.node_delay and self.player.web >= 100:
                            self.webNode_list.append(WebNode(self.player.pos.x, self.player.pos.y, self.webNode_list, self.connection_list))
                            # print "nodes:", len(self.webNode_list), ", connections:", len(self.connection_list)
                            if not DEBUG_MODE:
                                self.player.web -= 100
                            self.node_prev_ticks = self.game_time
                            self.sfx_web.play()
                            
                    if event.key in self.KEYS['attack']:
                        self.sfx_attack.play()
                        self.player.attack()
                        if (self.game_time - self.venom_prev_ticks) > self.venom_delay and self.player.venom >= 167:
                            for enemy in self.enemy_list:
                                if enemy.pos.distance(self.player.pos) <= 50 and enemy.stoptime > 0:
                                    # self.enemy_list.remove(enemy)
                                    self.sfx_kill.play()
                                    enemy.start_dying()
                                    if not DEBUG_MODE:
                                        self.player.venom -= 167
                                    self.player.attack()
                                    self.venom_prev_ticks = self.game_time
                                    if not self.game_over:
                                        self.score += 50
                                    break
                                    
                # End Game
                if self.game_over and not self.score_made:
                    if event.key in self.KEYS['left']:
                        self.HUD.name_input(4)
                    if event.key in self.KEYS['right']:
                        self.HUD.name_input(6)
                    if event.key in self.KEYS['up']:
                        self.HUD.name_input(8)
                    if event.key in self.KEYS['down']:
                        self.HUD.name_input(2)
                    if event.key in self.KEYS['confirm']:
                        self.HUD.make_score(self.score)
                        self.score_made = True
                        
    def reset_game(self):
        self.game_over = False
        self.score_made = False
        
        self.start_game()
        
        
    def update(self):
        if self.paused:
            self.pause_time = pygame.time.get_ticks() - self.game_time
        else:
            self.game_time = pygame.time.get_ticks() - self.pause_time
    
            if self.game_time - self.last_score_time > 1000:
                #self.last_score_time += 1000
                self.last_score_time = self.game_time
                if not self.game_over:
                    self.score += 5
        
            if self.game_time - self.spawn_wait_start_time > self.time_until_spawn:
                if random.random() < 0.02:
                    self.enemy_list.append(Enemy(self.game_time, self.egg_list))
                    self.enemies_spawned_this_wave += 1
                if self.enemies_spawned_this_wave == self.total_enemies_this_wave:
                    self.spawn_wait_start_time = self.game_time
                    if  self.wave_number % 3 == 0 :
                        self.total_enemies_this_wave += random.randint( 3, 5) * self.wave_number
                    
                    else:
                        self.total_enemies_this_wave += self.wave_number * 2 + random.randint(0, 4)
                        
                    self.enemies_spawned_this_wave = 0
                    # Reset timer
                    # self.timer = 20 + random.randint(-2*self.wave_number,2*self.wave_number)
                    self.timer_past_time = self.game_time
                    
                    self.time_until_spawn = random.randint(18000-1000*self.wave_number, 22000+1000*self.wave_number)
                    self.timer = self.time_until_spawn / 1000 + random.randint(-3*self.wave_number,3*self.wave_number)
                    if self.timer < 0:
                        self.timer = 0
                    
                    # print "time_until_spawn:", self.time_until_spawn
                    # print "timer:", self.timer
                    
                    
                    self.wave_number += 1
                    
            if self.game_time - self.timer_past_time > 1000:
                #self.timer_past_time += 1000
                self.timer_past_time = self.game_time
                if self.timer > 0:
                    self.timer -= 1
        
            self.player.update(self.game_time)
        
            for webNode in self.webNode_list:
                webNode.update()
                
            for egg in self.egg_list:
                egg.update()
                
            for enemy in self.enemy_list:
                enemy.update(self.game_time, self.enemy_list, self.connection_list)
                
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
                if enemy.reached_target_egg():
                    if len(self.egg_list) > 0:
                        self.sfx_egg_die.play()
                        # print enemy.goal_egg_object
                        # print enemy.goal_egg_object.id
                        self.egg_list[:] = [egg for egg in self.egg_list if not egg.id == enemy.goal_egg_object.id]
                        for enemy2 in self.enemy_list:
                            if enemy2 != enemy and enemy2.goal_egg_object.id == enemy.goal_egg_object.id:
                                enemy2.chooseGoal(self.egg_list)
                    
            # remove enemys that reached its target from the list and enemies that died
            self.enemy_list[:] = [enemy for enemy in self.enemy_list if not enemy.reached_target_egg() and not enemy.is_dead]
            
            if len(self.egg_list) == 0:
                self.game_over = True
        
    def delete_webNode(self, webNode_list_index):
        webNode = self.webNode_list[webNode_list_index]
        
        webNode.delete_all_connections(self.connection_list)
        self.webNode_list.pop(webNode_list_index)
        
        for enemy in self.enemy_list:
            if not enemy.stuckTo in self.connection_list:
                enemy.break_loose(self.game_time)
        
    def draw(self):
        self.screen.fill((30,30,30))
        self.game_screen.fill((80,80,80))
        self.screen.blit( self.hud_bg, pygame.Rect(768, 0, self.hud_bg.get_width(), self.hud_bg.get_height()))
        self.game_screen.blit( self.game_bg, pygame.Rect(0, 0, self.game_bg.get_width(), self.game_bg.get_height()))
        
        # before = pygame.time.get_ticks()
        
        for connection in self.connection_list:
            connection.draw(self.game_screen)
        
        
        # after = pygame.time.get_ticks()
            
        # print after - before, "millis"
        
        
        for webNode in self.webNode_list:
            webNode.draw(self.game_screen)
        
        for egg in self.egg_list:
            egg.draw(self.game_screen)
        
        for enemy in self.enemy_list:
            enemy.draw(self.game_screen)
        
        # redraw the player object (above all other objects)
        self.player.draw(self.game_screen)
        
        self.screen.blit(self.game_screen, (0, 0))
        
        # HUD
        self.HUD.draw(self.screen, self.player, self.timer, len(self.egg_list), self.score, self.game_over, self.score_made)
        
        if self.score_made:
            self.HUD.print_scores(self.screen)
            
        if self.paused:
            self.screen.blit(self.pause_screen, (0, 0))
        
        
# ---------------------------------------------------------------------------------------    


# ---------------------------------------------------------------------------------------    
# Overall game logic. Creates a Game object and calls its functions in order, draws to the screen

pygame.init()
pygame.display.set_caption("Motherly Instinct")
g = Game()
pygame.key.set_repeat(500, 200)

# g.splash_screen()

while not g.game_exit:
    g.clock.tick(30)
    g.process_events()
    g.update()
    g.draw()
    pygame.display.flip()

    
sys.exit()
    
    
    
    
    
    
