import pygame, os
from time import localtime, strftime, time
from operator import attrgetter
from utilities import *
from globals import *

class HUD(object):

    def __init__(self):
        self.web_base = pygame.image.load(resource_path(os.path.join('HUD', 'web-base.png'))).convert_alpha()
        self.web_rect = pygame.Rect(857,100,self.web_base.get_width(),self.web_base.get_height())
        self.web_fill = pygame.image.load(resource_path(os.path.join('HUD', 'web-fill.png'))).convert_alpha()
        
        self.venom_base = pygame.image.load(resource_path(os.path.join('HUD', 'venom-base.png'))).convert_alpha()
        self.venom_rect = pygame.Rect(911,100,self.venom_base.get_width(),self.venom_base.get_height())
        self.venom_fill = pygame.image.load(resource_path(os.path.join('HUD', 'venom-fill.png'))).convert_alpha()
        
        self.egg = pygame.image.load(resource_path('eggs.png')).convert_alpha()
        
        self.font = pygame.font.Font(resource_path(os.path.join('HUD', 'Spiderfingers.ttf')), 42)
        self.font_small = pygame.font.Font(resource_path(os.path.join('HUD', 'Spiderfingers.ttf')), 24)
        
        self.initials = [0, 0, 0]
        self.initials_index = 0
    
    
    def draw(self, screen, player, timer, eggs, score, game_over, score_made):
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
            txt = self.font.render("GAME OVER", True, (172,0,0))
            x = GAME_WIDTH/2-txt.get_width()/2
            y = GAME_HEIGHT/2-txt.get_height()/2
            screen.blit(txt, pygame.Rect( x, y, 100, 42))

        # Initials Input
        if game_over and not score_made:
            txt = self.font.render("WWW", True, (200,200,200))
            # x = 768+(128 - txt.get_width()/2)
            # y = 494+26+75
            x = GAME_WIDTH/2-txt.get_width()/2
            y = GAME_HEIGHT/2-txt.get_height()/2+75
            for i in range(0, len(self.initials)):
                c = (200,200,200)
                if self.initials_index == i:
                    c = (172,0,0)
                txt = self.font.render(chr(self.initials[i]+65), True, c)
                screen.blit(txt, pygame.Rect( x+69*i/2.0-txt.get_width()/2, y, 100, 42))
                
                
    def name_input(self, dir):
        # Left
        if dir == 4:
            self.initials_index = (self.initials_index - 1) % 3
        # Right
        if dir == 6:
            self.initials_index = (self.initials_index + 1) % 3
        # Up
        if dir == 8:
            self.initials[self.initials_index] = (self.initials[self.initials_index] - 1) % 26
        # Down
        if dir == 2:
            self.initials[self.initials_index] = (self.initials[self.initials_index] + 1) % 26
        # Enter name
        if dir == 5:
            make_score()
            
    def make_score(self, score):
        name = ""
        for i in range(0, len(self.initials)):
            name += chr(self.initials[i]+65)
        self.my_score = Score(score, name)
        
        self.all_scores = []
        # Add my score to list
        self.all_scores.append(self.my_score)
        if os.path.exists(highscore_path()):
            with open(highscore_path(), 'r') as f:
                rows = f.readlines()
                # Read all scores
                for r in rows:
                    blocks = r.strip().split(' ')
                    a_score = Score(blocks[0], blocks[1])
                    a_score.time = blocks[2]
                    self.all_scores.append(a_score)
            # Sort all scores
            self.all_scores = sorted(self.all_scores, key=lambda score: (int(score.score), -float(score.time)), reverse = True)
        # Write first 100 scores
        with open(highscore_path(), 'w') as f:
            for i in range(0, min(len(self.all_scores), 100)):
                a_score = str(self.all_scores[i].score) + " " + self.all_scores[i].initials + " " + str(self.all_scores[i].time) + "\n"
                f.write(a_score)
                
                
    def print_scores(self, screen):
        s = pygame.Surface((GAME_WIDTH*2/3,GAME_HEIGHT))
        s.set_alpha(200)
        s.fill((30,30,30))
        screen.blit(s, (GAME_WIDTH/6,0))
        # Rank  Score   Name
        y = 100
        c = (240,240,240)
        txt = self.font.render("Rank \t\t Score \t\t Name", True, c)
        x = GAME_WIDTH/2 - txt.get_width()/2
        screen.blit(txt, pygame.Rect( x, y-66, 100, 42))
        for i in range(0, len(self.all_scores)):
            # My score? :OOO
            if self.my_score.time == self.all_scores[i].time and self.my_score.score == self.all_scores[i].score and self.my_score.initials == self.all_scores[i].initials:
                my_rank = i
                break
        for i in range(0, len(self.all_scores)):
            c = (200,200,200)
            if i == my_rank:
                c = (172,0,0)
            # Rank
            txt = self.font.render(str(i+1), True, c)
            screen.blit(txt, pygame.Rect( x, y+42*i, 100, 42))
            # Score
            score_text = str(self.all_scores[i].score).zfill(5)
            for j in range(0, len(score_text)):
                digit = int(self.all_scores[i].score) / (10**(len(score_text)-1-j)) % 10
                txt = self.font.render(str(digit), True, c)
                screen.blit(txt, pygame.Rect( x + 90 + 24*j, y+42*i, 100, 42))
            # Name
            txt = self.font.render(str(self.all_scores[i].initials), True, c)
            screen.blit(txt, pygame.Rect( x + 250, y+42*i, 100, 42))
            if i == 9:
                break
        # If my score is not in the top 10...
        if my_rank >= 10:
            c = (240,240,240)
            txt = self.font.render("\t\t\t\t\t\t\t\t\t\t\t\t\t\t", True, c)
            screen.blit(txt, pygame.Rect( x, y+42*10+10, 100, 42))
            c = (172,0,0)
            # Rank
            if my_rank < 100:
                txt = self.font.render(str(my_rank+1), True, c)
            else:
                txt = self.font.render("--", True, c)
            screen.blit(txt, pygame.Rect( x, y+42*11, 100, 42))
            # Score
            score_text = str(self.all_scores[my_rank].score).zfill(5)
            for j in range(0, len(score_text)):
                digit = int(self.all_scores[my_rank].score) / (10**(len(score_text)-1-j)) % 10
                txt = self.font.render(str(digit), True, c)
                screen.blit(txt, pygame.Rect( x + 90 + 24*j, y+42*11, 100, 42))
            # Name
            txt = self.font.render(str(self.all_scores[my_rank].initials), True, c)
            screen.blit(txt, pygame.Rect( x + 250, y+42*11, 100, 42))
            
        
        
class Score(object):
    def __init__(self, score, initials):
        self.score = score
        self.initials = initials
        self.time = time()


