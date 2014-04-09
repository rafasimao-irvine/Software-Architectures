import pygame
import math
from consts import Consts

class Sprite(object):

    def __init__(self, image_path, number_of_frames, delay): 
        #images informations
        self.image_path = image_path
        self.image = pygame.image.load(image_path)
        
        self.image_rect = self.image.get_rect()
        self.image_rect.width /= number_of_frames
        self.initial_image_x = self.image_rect.x
        
        #frames informations
        self.number_of_frames = number_of_frames
        self.current_frame = 0
        
        #times informations
        self.delay = delay
        self.time = pygame.time.get_ticks()
        self.passed_time = 0;
        
        #number of loops through the sprite
        self.number_of_plays = 0

    
    def _update(self): 
        
        if((self.number_of_plays > 0) or 
           (self.number_of_plays == Consts.PLAY_INFINITY)):
            #updates passed time
            self.passed_time += pygame.time.get_ticks() - self.time

            frame_skip = math.floor(self.passed_time/self.delay)#calculates how many frames will be skipped

            #skip the frames
            self.current_frame += frame_skip
            #verifies the loops it had already made
            if (self.number_of_plays != Consts.PLAY_INFINITY):
                self.number_of_plays -= math.floor(self.current_frame/self.number_of_frames)#reduces the number of loops
                if(self.number_of_plays < 0): self.number_of_plays = 0#To be sure it is not going to the infinity
            #calibrates the current sprite
            self.current_frame %= self.number_of_frames
        
            #next passed time
            self.passed_time %= self.delay
        
            #updates last time
            self.time = pygame.time.get_ticks() 
    

    def _render(self, screen, position):
        self.image_rect.x = self.initial_image_x + self.image_rect.width * self.current_frame
        screen.blit(self.image, position, self.image_rect)
    
    #starts the sprite to play
    def _play(self, number_of_plays):
        #if it's a valid number
        if (number_of_plays > -2):
            self.time = pygame.time.get_ticks()
            self.passed_time = 0;
            
            self.number_of_plays = number_of_plays
            
    def is_playing(self):
        if((self.number_of_plays > 0) or 
           (self.number_of_plays == Consts.PLAY_INFINITY)):
            return True
        else:
            return False  