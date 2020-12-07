'''
Created on 05/03/2014
Main class of the game.

@author: rafaelsimao, alfonsoaranzazu
'''

import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'

#import sys 
import pygame
from consts import Consts
from stateItemsBoard import StateItemsBoard
from stateFight import StateFight
from inputManager import InputManager
from character import Character

#initiate the pygame
pygame.init()
fpsClock = pygame.time.Clock()
#print("initializing clock: ", fpsClock)

#Manager class
class Manager:

    ##Screen
    width, height = 950, 600
    size = width, height
    
    screen  = pygame.display.set_mode(size)
    pygame.display.set_caption("StepFight")        
    
    #InputManager
    inputManager = InputManager()
    character = Character()
    
    #Initial state
    state = StateItemsBoard(screen, inputManager, character)
     
    #Main Loop
    def _run(self):
        self.gameOn = True
        
        while self.gameOn:
            
            #Inputs
            self.inputManager.update()
            
            #Updates
            self._update()
                
            #Renders, put in the screen
            self._render()
            
            fpsClock.tick(30)
        
    
    #Update
    def _update(self):
        #state updates
        new_state = self.state._update()
        if (new_state == Consts.STATE_CONTINUE):
            return
        
        elif (new_state == Consts.STATE_ITEMS_BOARD):
            self.state.destroy()
            self.state = StateItemsBoard(self.screen,self.inputManager,self.character)
        
        elif (new_state == Consts.STATE_FIGHT):
            self.state.destroy()
            self.state = StateFight(self.screen,self.inputManager,self.character)
            
    #Render
    def _render(self):
        #state renders
        self.state._render()
        
        #updates the display
        pygame.display.update()
        
        

#Run the main loop
if "__main__" == __name__:
    
    manager = Manager()
    manager._run()

