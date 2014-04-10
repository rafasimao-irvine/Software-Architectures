#class used to show the items board and it's procedures
import pygame
from state import State
from button import Button
from buttonListener import ButtonListener
from consts import Consts

class StateItemsBoard(State, ButtonListener):
    
    PLAY_BUTTON = 1
    BUY_SWORD_BUTTON = 2
    BUY_HELMET_BUTTON = 3
    BUY_ARMOR_BUTTON = 4
    BUY_SPELL_BUTTON = 5

    def __init__(self, screen, inputManager, character):
        State.__init__(self, screen, inputManager)
        self.character = character;
        
        self.width, self.height = self.screen.get_width(), self.screen.get_height()    
        pygame.display.set_caption("StepFight - Items Menu")
        
        #Items Box dimensions
        self.item_width, self.item_height = 250, 200
        self.item_screen = self.item_width, self.item_height
        
        #Fonts
        self.font_object = pygame.font.Font('freesansbold.ttf', 20)
        
        self.next_state = Consts.STATE_CONTINUE
        
        #Play button
        self.play_button = self._createButton(self.PLAY_BUTTON, Consts.PLAY, (700,525,200,50))
        self.play_button.font_object = pygame.font.Font('freesansbold.ttf', 35)
        self.play_button._setPadding(50, 10)
    
        #Buy buttons
        self.buy_sword_button = self._createButton(self.BUY_SWORD_BUTTON, Consts.BUY, (75, 200,100,40))
        self.buy_helmet_button = self._createButton(self.BUY_HELMET_BUTTON, Consts.BUY, (525, 200,100,40))
        self.buy_armor_button = self._createButton(self.BUY_ARMOR_BUTTON, Consts.BUY, (75, 450,100,40))
        self.buy_spell_button = self._createButton(self.BUY_SPELL_BUTTON, Consts.BUY, (525, 450,100,40))
    
    def destroy(self):
        self.inputManager.detach(self.play_button)
        self.inputManager.detach(self.buy_sword_button)
        self.inputManager.detach(self.buy_helmet_button)
        self.inputManager.detach(self.buy_armor_button)
        self.inputManager.detach(self.buy_spell_button)
    
    def _createButton(self, button_id, message, rect):
        button = Button(button_id, self, message, Consts.LIGHT_GOLD_COLOR, rect)
        self.inputManager.attach(button)
        button.font_object = self.font_object
        button._setColors(Consts.LIGHT_GOLD_COLOR, Consts.HOVER_GOLD_COLOR, Consts.PRESSED_GOLD_COLOR)
        
        return button
        
    def receiveInput(self, event):
        State.receiveInput(self, event)
    
    def _update(self):
        State._update(self)
        #update buttons
        self.play_button._update()
        
        self.buy_sword_button._update()
        self.buy_helmet_button._update()
        self.buy_armor_button._update()
        self.buy_spell_button._update()
        
        return self.next_state
        
    def _render(self):
        State._render(self)
        
        #Draws the entire menu
        self.draw_items_menu()
        self.print_level()
        
        #render buttons
        self.play_button._render(self.screen)
        
        self.buy_sword_button._render(self.screen)
        self.buy_helmet_button._render(self.screen)
        self.buy_armor_button._render(self.screen)
        self.buy_spell_button._render(self.screen)
        
    def draw_items_menu(self):
        self.screen.fill(Consts.LIGHT_GOLD_COLOR)
        
        self.draw_items_boxes()
        self.display_items_images()
        self.display_items_descriptions()
        #self.display_buy_buttons()
        
        self.display_starting_gold(self.character.money)
        #self.display_play_button()
        
        
    def draw_items_boxes(self):
        start_x, start_y = (50, 50)
        end_x, end_y = (400, 200)

        # draws the 4 boxes
        for i in range(4):
            pygame.draw.rect(self.screen, Consts.BLACK_COLOR, ( start_x, start_y, end_x, end_y), 5)
            start_x += 450
            if i == 1:
                start_x = 50
                start_y += 250

    def display_items_images(self):
        image_list = [Consts.SWORD_IMAGE, Consts.HELMET_IMAGE, Consts.ARMOR_IMAGE, Consts.SPELL_BOOK_IMAGE]
        start_x, start_y = 75, 75
        end_x, end_y = 100, 100
        
        counter = 0
        for image in image_list:
            image_rect = image.get_rect()
            image_rect.topleft = (start_x, start_y)
            self.screen.blit(image, image_rect)
            start_x += 450
            counter += 1
            if counter == 2:
                start_x = 75
                start_y += 250
                
    def display_buy_buttons(self):
        start_x, start_y = 75, 200
        end_x, end_y = 100, 40
        for i in range(4):
            pygame.draw.rect(self.screen, Consts.BLACK_COLOR, (start_x, start_y, end_x, end_y), 5)
            buy = self.font_object.render(Consts.BUY, False, Consts.BLACK_COLOR)
            buy_rect = buy.get_rect()
            buy_rect.topleft = (start_x + 10, start_y + 10)
            self.screen.blit(buy, buy_rect)
            start_x += 450
            if i == 1:
                start_x = 75
                start_y += 250
                
#    def display_play_button(self):
#        start_x, start_y = 700, 525
#        end_x, end_y = 200, 50
#        play_button = pygame.draw.rect(self.screen, Consts.BLACK_COLOR, (start_x, start_y, end_x, end_y), 5)
#        
#        my_font = pygame.font.Font('freesansbold.ttf', 35)
#        
#        play = my_font.render(Consts.PLAY, False, Consts.BLACK_COLOR)
#        play_rect = play.get_rect()
#        play_rect.topleft = (start_x + 50, start_y + 10)
#        self.screen.blit(play, play_rect)
                
    def display_items_descriptions(self):
        descriptions_list = [Consts.SWORD_DESCRIPTION, Consts.HELMET_DESCRIPTION, Consts.ARMOR_DESCRIPTION, Consts.SPELL_BOOK_DESCRIPTION]
        price_list = [Consts.SWORD_PRICE, Consts.HELMET_PRICE, Consts.ARMOR_PRICE, Consts.SPELL_PRICE]
        start_x, start_y = 200, 100
        end_x, end_y = 100, 100
        my_font = pygame.font.Font('freesansbold.ttf', 30)
        
        counter = 0
        for description in descriptions_list:
            msg_surface = my_font.render(description, False, Consts.BLACK_COLOR)
            msg_rect = msg_surface.get_rect()
            msg_rect.topleft = (start_x, start_y)
            self.screen.blit(msg_surface, msg_rect)
            #price
            pygame.draw.circle(self.screen, Consts.GOLD_COLOR, (start_x+80, start_y+88), 10)
            pygame.draw.circle(self.screen, Consts.BLACK_COLOR, (start_x+80, start_y+88), 11, 2)
            msg_surface = self.font_object.render(str(price_list[counter]), False, Consts.BLACK_COLOR)
            msg_rect = msg_surface.get_rect()
            msg_rect.topleft = (start_x+100, start_y+80)
            self.screen.blit(msg_surface, msg_rect)
            start_x += 450
            counter += 1
            if counter == 2:
                start_x = 200
                start_y = 350
                
        
    def display_starting_gold(self, player_gold):
        msg1 = "My Gold"
        my_font_object = pygame.font.Font('freesansbold.ttf', 30)
        msg_surface_object = my_font_object.render(msg1, False, Consts.BLACK_COLOR)
        msg_rect_object = msg_surface_object.get_rect()
        msg_rect_object.topleft = (50, 550)

        pygame.draw.circle(self.screen, Consts.GOLD_COLOR, (220, 560), 15)
        pygame.draw.circle(self.screen, Consts.BLACK_COLOR, (220, 560), 16, 2)
        
        gold_surface_object = my_font_object.render(str(player_gold), False, Consts.BLACK_COLOR)
        gold_rect_object = gold_surface_object.get_rect()
        gold_rect_object.topleft = (250, 550)
                
        self.screen.blit(msg_surface_object, msg_rect_object)
        self.screen.blit(gold_surface_object, gold_rect_object)
       
       
    def print_level(self):
        msg_surface_object = self.font_object.render("Lvl "+str(self.character.level), False, Consts.BLACK_COLOR)
        msg_rect_object = msg_surface_object.get_rect()
        msg_rect_object.topleft = (50, 20)
        self.screen.blit(msg_surface_object, msg_rect_object)
        
    def clickPerformed(self, button_id): 
        if(button_id == self.PLAY_BUTTON):
            self.next_state = Consts.STATE_FIGHT
        
        elif(button_id == self.BUY_SWORD_BUTTON):
            if(self.character.money >= Consts.SWORD_PRICE):
                self.buy_sword_button.is_activated = False
                self.character.strength += Consts.SWORD_BONUS
                self.character.money -= Consts.SWORD_PRICE
        
        elif(button_id == self.BUY_HELMET_BUTTON):
            if(self.character.money >= Consts.HELMET_PRICE):
                self.buy_helmet_button.is_activated = False
                self.character.defence += Consts.HELMET_BONUS
                self.character.money -= Consts.HELMET_PRICE
        
        elif(button_id == self.BUY_ARMOR_BUTTON):
            if(self.character.money >= Consts.ARMOR_PRICE):
                self.buy_armor_button.is_activated = False
                self.character.defence += Consts.ARMOR_BONUS
                self.character.money -= Consts.ARMOR_PRICE

        elif(button_id == self.BUY_SPELL_BUTTON):
            if(self.character.money >= Consts.SPELL_PRICE):
                self.buy_spell_button.is_activated = False
                self.character.magic += Consts.SPELL_BONUS
                self.character.money -= Consts.SPELL_PRICE
            
            
        