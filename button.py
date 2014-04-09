import pygame
from inputListener import InputListener
# from buttonListener import ButtonListener
from consts import Consts

class Button(InputListener):

    def __init__(self, button_id, button_listener, message, color, button_rect):
        self.button_id = button_id
        
        self.button_listener = button_listener
        
        self.message = message
        
        self.color = color
        self.button_rect  = pygame.Rect(button_rect)
        
        self.hovered_color = color
        self.pressed_color = color
        self.is_pressed = self.is_hovered = False
                
        self.border_color = Consts.BLACK_COLOR
        self.border_width = 5
        
        self.text_color = Consts.BLACK_COLOR

        #Fonts
        self.font_object = pygame.font.Font('freesansbold.ttf', 20)
        
        #Paddings
        self.left_padding = self.button_rect.w*0.2
        self.top_padding  = self.button_rect.h*0.38
        
        self.is_activated = True
        
    #set the button colors    
    def _setColors(self, color, hovered_color, pressed_color):
        self.color = color
        self.hovered_color = hovered_color
        self.pressed_color = pressed_color
        
    #set the button paddings 
    def _setPadding(self, left_padding, top_padding):
        self.left_padding = left_padding
        self.top_padding = top_padding
    
    #receives the mouse input    
    def receiveInput(self, event):
        #sees if it is activated
        if(not self.is_activated):
            return
        
        #Sees if it is pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(self._isOverButton(pygame.mouse.get_pos())):
                self.is_pressed = True
                self.is_hovered = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if(self.is_pressed):
                self.is_pressed = False
                if(self._isOverButton(pygame.mouse.get_pos())):
                    self.button_listener.clickPerformed(self.button_id)
        
        #sees if it is hovered            
        if (self._isOverButton(pygame.mouse.get_pos())):
            if(not self.is_pressed):
                self.is_hovered = True
        else: self.is_hovered = False
    
    #updates
    def _update(self):
        pass
    
    #renders the button in the screen
    def _render(self, screen):  
        #Button itself
        if(self.is_pressed or not self.is_activated):
            pygame.draw.rect(screen, self.pressed_color, self.button_rect)
        elif(self.is_hovered):
            pygame.draw.rect(screen, self.hovered_color, self.button_rect)
        else:
            pygame.draw.rect(screen, self.color, self.button_rect)
        
        #Border
        pygame.draw.rect(screen, self.border_color, self.button_rect, self.border_width)
        
        #Message
        message_rect = pygame.Rect(self.button_rect)
        message_rect.topleft = (self.button_rect.x + self.left_padding ,self.button_rect.y + self.top_padding)
        screen.blit(self.font_object.render(self.message, False, self.text_color), message_rect)
        
 
    #sees if the point is over the button
    def _isOverButton(self, point_position):
        if(self.button_rect.collidepoint(point_position)):
            return True
        else: 
            return False
        
        
        