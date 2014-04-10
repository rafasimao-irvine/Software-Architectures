import pygame
import random
from sprite import Sprite
from consts import Consts

class Dragon(object):
    
    FULL_LIFE = 15.0
    
    ATTACK_CHANCE = 0.4
    DEFENSE_CHANCE = 0.7
    CHARGE_CHANCE = 0.9
    SPELL_CHANCE = 1

    def __init__(self, level):
        #Character images
        self.sprite_attack = Sprite(Consts.DRAGON_ATTACK, 10, 120)
        self.sprite = Sprite(Consts.DRAGON_STILL, 10, 100)
        self.sprite._play(Consts.PLAY_INFINITY)
        
        self.sprite_defense = Sprite(Consts.SPRITE_DEFENSE, 25, 70)
        self.sprite_charge = Sprite(Consts.SPRITE_CHARGE, 11, 90)
        
        #self.sprite_spell = Sprite(Consts.SPELL_DRAGON, 25, 90)
        
        #Attributes
        if(level > 1):
            self.setAttributes(level, level, 5+level)
        else:
            self.setAttributes(1, 1, 5)
            
        #life
        self.life = self.FULL_LIFE
        self.lifebar_rect = pygame.Rect(Consts.DRAGON_POSITION[0]+14,Consts.DRAGON_POSITION[1]+8,225,13)
        
        self.charged = 1
        
    def setAttributes(self, strength, defence, magic):
        self.strength = strength
        self.defence = defence
        self.magic = magic
        
    def update(self):
        self.sprite_attack._update()
        self.sprite._update()
        
        self.sprite_defense._update()
        self.sprite_charge._update()
        
        #self.sprite_spell._update()
        
        
    def render(self, screen):
        #character
        if(self.sprite_attack.is_playing()):
            self.sprite_attack._render(screen, Consts.DRAGON_POSITION)
        else:
            self.sprite._render(screen, Consts.DRAGON_POSITION)
        
        if(self.sprite_defense.is_playing()):
            self.sprite_defense._render(screen, (Consts.DRAGON_POSITION[0]+30, Consts.DRAGON_POSITION[1]+30))
            
        if(self.sprite_charge.is_playing()):
            self.sprite_charge._render(screen, (Consts.DRAGON_POSITION[0]+30,Consts.DRAGON_POSITION[1]+30))
        #if(self.sprite_spell.is_playing()):
        #    self.sprite_spell._render(screen, Consts.CHARACTER_POSITION)
        
            
        #lifebar
        if(self.life>0):
            current_lifebar_rect = pygame.Rect(self.lifebar_rect)
            current_lifebar_rect.width = (self.life/self.FULL_LIFE)*self.lifebar_rect.width
            pygame.draw.rect(screen, Consts.RED_COLOR, current_lifebar_rect)
        pygame.draw.rect(screen, Consts.BLACK_COLOR, self.lifebar_rect, 2)
        
        

    def attack(self):
        self.sprite_attack._play(1)
        
    def defense(self):
        self.sprite_defense._play(1)
            
    def spell(self): pass
        #self.sprite_spell._play(1)
    
    def charge(self):
        self.charged *= 2
        self.sprite_charge._play(1)
        
    def unCharge(self):
        load = self.charged
        self.charged = 1
        return load
        
    def getMovement(self):
        rand = random.random()
        
        result = 0
        if(rand<self.ATTACK_CHANCE):
            result = Consts.ATTACK
        elif(rand<self.DEFENSE_CHANCE):
            result = Consts.DEFENSE
        elif(rand<self.CHARGE_CHANCE):
            result = Consts.SPELL
        else:
            result = Consts.CHARGE
            
        return result
        
    def beHitted(self, damage):
        if(damage>0):
            self.life -= damage
    
    def isDead(self):
        if(self.life<1):
            return True
        return False