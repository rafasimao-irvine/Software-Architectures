#class used to show the fight part of the game
import pygame
from state import State
from button import Button
from buttonListener import ButtonListener
from character import Character
from dragon import Dragon
from consts import Consts

class StateFight(State, ButtonListener):
    
    ATTACK_BUTTON = 1
    DEFENSE_BUTTON = 2
    SPELL_BUTTON = 3
    CHARGE_BUTTON = 4
    CONTINUE_BUTTON = 5
    
    RUN_BUTTON = 10

    def __init__(self, screen, inputManager, character):
        State.__init__(self, screen, inputManager)
        self.character = character;
        self.character.reset()
        
        pygame.display.set_caption("StepFight - Dragon Fight")
        
        self.background = pygame.image.load(Consts.FIGHT_BACKGROUND)
        
        #Create buttons
        self._createButtons()
        #Create characters
        #self.character = Character()
        self.dragon = Dragon(character.level)
        
        self.is_in_resolution = False
        self.text_character_attack = ""
        self.text_dragon_attack = ""
        self.font_object = pygame.font.Font('freesansbold.ttf', 20)
        
        self.fight_ended = False
        
        self.next_state = Consts.STATE_CONTINUE
    
    def destroy(self):
        self.inputManager.detach(self.attack_button)
        self.inputManager.detach(self.defense_button)
        self.inputManager.detach(self.spell_button)
        self.inputManager.detach(self.charge_button)
        self.inputManager.detach(self.run_button)
        self.inputManager.detach(self.continue_button)
    
    def _createButtons(self):
        #Attack button
        self.attack_button = self._createButton(self.ATTACK_BUTTON, "Attack", (80,510,150,50))
        #Defense button
        self.defense_button = self._createButton(self.DEFENSE_BUTTON, "Defense", (280,510,150,50))
        #Spell button
        self.spell_button = self._createButton(self.SPELL_BUTTON, "Spell", (480,510,150,50))
        if(self.character.magic == 0):
            self.spell_button.is_activated = False
        #Charge button
        self.charge_button = self._createButton(self.CHARGE_BUTTON, "Charge", (680,510,150,50))
        
        #Run button
        self.run_button = self._createButton(self.RUN_BUTTON, "Run!", (50,50,60,30))
        self.run_button._setPadding(7, 8)
        self.run_button._setColors(Consts.RED_COLOR, Consts.HOVER_RED_COLOR, Consts.PRESSED_RED_COLOR)
        self.run_button.text_color = Consts.WHITE_COLOR
        
        self.continue_button = self._createButton(self.CONTINUE_BUTTON, "Continue", (700,510,150,50))
        self.continue_button.is_activated = False
        
    def _createButton(self, button_id, message, rect):
        button = Button(button_id, self, message, Consts.GRAY_COLOR, rect)
        self.inputManager.attach(button)
        button.border_color = Consts.WHITE_COLOR
        button._setColors(Consts.GRAY_COLOR, Consts.HOVER_GRAY_COLOR, Consts.PRESSED_GRAY_COLOR)
        
        return button
    
    def receiveInput(self, event):
        State.receiveInput(self, event)
    
    
    def _update(self):
        State._update(self)
        
        if(not self.fight_ended and (self.character.isDead() or self.dragon.isDead()) ):
            self.fight_ended = True
            self.enterResolutionMode()
            if(not self.character.isDead()):
                self.character.level += 1
                self.character.money += 150
        
        #buttons
        if(self.is_in_resolution):
            self.continue_button._update()
        else:
            self.attack_button._update()
            self.defense_button._update()
            self.spell_button._update()
            self.charge_button._update()
        
        self.run_button._update()
        #characters
        self.character.update()
        self.dragon.update()
        
        return self.next_state
        
        
    def _render(self):
        State._render(self) 
        #background
        self.screen.fill(Consts.BLACK_COLOR)
        self.screen.blit(self.background, self.background.get_rect())
        
        #buttons
        if(self.is_in_resolution):
            self.continue_button._render(self.screen)
            if(self.fight_ended):
                self.font_object = pygame.font.Font('freesansbold.ttf', 30)
                if(self.character.isDead()):
                    self.screen.blit(self.font_object.render("YOU LOST...", False, Consts.RED_COLOR), (270,520))
                else:
                    self.screen.blit(self.font_object.render("YOU WON!!!!!", False, Consts.GOLD_COLOR), (270,520))
            else:
                message = "You"+self.text_character_attack
                self.screen.blit(self.font_object.render(message, False, Consts.WHITE_COLOR), (50,510))
                message = "Dragon"+self.text_dragon_attack
                self.screen.blit(self.font_object.render(message, False, Consts.WHITE_COLOR), (50,550))
        else:
            self.attack_button._render(self.screen)
            self.defense_button._render(self.screen)
            self.spell_button._render(self.screen)
            self.charge_button._render(self.screen)
        
        self.run_button._render(self.screen)
        #characters
        self.dragon.render(self.screen)
        self.character.render(self.screen)
        
        self.print_level()
    
    def print_level(self):
        msg_surface_object = self.font_object.render("Lvl "+str(self.character.level), False, Consts.BLACK_COLOR)
        msg_rect_object = msg_surface_object.get_rect()
        msg_rect_object.topleft = (50, 20)
        self.screen.blit(msg_surface_object, msg_rect_object)    
        
    def clickPerformed(self, button_id):
        #character movement
        character_movement = 0
        if(button_id == self.ATTACK_BUTTON): 
            character_movement = Consts.ATTACK
        elif(button_id == self.DEFENSE_BUTTON):
            character_movement = Consts.DEFENSE
        elif(button_id == self.SPELL_BUTTON):
            character_movement = Consts.SPELL
        elif(button_id == self.CHARGE_BUTTON):
            character_movement = Consts.CHARGE
            
        elif(button_id == self.CONTINUE_BUTTON):
            if(self.fight_ended):
                self.next_state = Consts.STATE_ITEMS_BOARD
            self.enterBattleMode()
            character_movement = 0
        
        elif(button_id == self.RUN_BUTTON):
            self.next_state = Consts.STATE_ITEMS_BOARD        

        if(character_movement != 0):
            self.resolveFight(character_movement)
            
            
    def resolveFight(self, character_movement):
        #dragons movement
        dragon_movement = self.dragon.getMovement()

        character_def = dragon_def = 0
        character_atk = dragon_atk = 0
        #character
        if(character_movement == Consts.DEFENSE):
            self.character.defense()
            character_def = self.character.defence
        elif(character_movement == Consts.ATTACK):
            self.character.attack()
            character_atk = self.character.strength*self.character.unCharge()
        elif(character_movement == Consts.SPELL):
            self.character.spell()
            character_atk = self.character.magic*self.character.unCharge()
        elif(character_movement == Consts.CHARGE):
            self.character.charge()

        #dragon
        if(dragon_movement == Consts.DEFENSE):
            self.dragon.defense()
            dragon_def = self.dragon.defence
        elif(dragon_movement == Consts.ATTACK):
            self.dragon.attack()
            dragon_atk = self.dragon.strength*self.dragon.unCharge()
        elif(dragon_movement == Consts.SPELL):
            self.dragon.spell()
            self.character.receive_spell()
            dragon_atk = self.dragon.magic*self.dragon.unCharge()
        elif(dragon_movement == Consts.CHARGE):
            self.dragon.charge()
            
        #resolve the damage
        self.dragon.beHitted(character_atk - dragon_def)
        self.character.beHitted(dragon_atk - character_def)

        #set in resolution mode
        self.enterResolutionMode()
        self.text_character_attack = self.getAttackText(character_movement, character_atk - dragon_def)
        self.text_dragon_attack = self.getAttackText(dragon_movement, dragon_atk - character_def)

        #DEBUG
        #print("character move: "+str(character_movement)+" dragon move: "+str(dragon_movement))
        #print("character atk: "+str(character_atk)+" dragon atk: "+str(dragon_atk))
        #print("character def: "+str(character_def)+" dragon def: "+str(dragon_def))
        #print("character life: "+str(self.character.life)+" dragon life: "+str(self.dragon.life))


    def getAttackText(self, move, damage):
        text = ""
        if(move == Consts.ATTACK):
            text = " attacked -  Damage: "+str(damage)
        elif(move == Consts.DEFENSE):
            text = " defended"
        elif(move == Consts.SPELL):
            text = " used a spell -  Damage: "+str(damage)
        elif(move == Consts.CHARGE):
            text = " charged!! "
            
        return text


    def enterResolutionMode(self):
        self.is_in_resolution = True
        self.continue_button.is_activated = True
        self.attack_button.is_activated = False
        self.defense_button.is_activated = False
        self.spell_button.is_activated = False
        self.charge_button.is_activated = False
        
    def enterBattleMode(self):
        self.is_in_resolution = False
        self.continue_button.is_activated = False
        self.attack_button.is_activated = True
        self.defense_button.is_activated = True
        self.spell_button.is_activated = True
        if(self.character.magic == 0):
            self.spell_button.is_activated = False
        self.charge_button.is_activated = True