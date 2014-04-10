import pygame
from sprite import Sprite
from consts import Consts

class Character(object):

    FULL_LIFE = 10.0
    
    counter = 0

    def __init__(self):
        #Character images
        self.sprite_attack = Sprite(Consts.CHARACTER_ATTACK, 6, 150)
        self.sprite = Sprite(Consts.CHARACTER_STILL, 1, 100)
        
        self.sprite_defense = Sprite(Consts.SPRITE_DEFENSE, 25, 70)
        self.sprite_charge = Sprite(Consts.SPRITE_CHARGE, 11, 90)
        
        self.sprite_spell = Sprite(Consts.SPELL_CHARACTER, 30, 70)
        
        self.sprite_spell_dragon = Sprite(Consts.SPELL_DRAGON, 25, 90)
        
        #Attributes
        self.strength = self.defence = self.magic = 0
        self.setAttributes(1, 1, 0)
        #life
        self.life = self.FULL_LIFE
        self.lifebar_rect = pygame.Rect(Consts.CHARACTER_POSITION[0]-15,Consts.CHARACTER_POSITION[1]+146,150,13)
        
        self.charged = 1
        
        self.level = 1
        
        self.money = 1000
        
    def setAttributes(self, strength, defence, magic):
        self.strength = strength
        self.defence = defence
        self.magic = magic
        
    def update(self):
        self.sprite._update()
        self.sprite_attack._update()
        
        self.sprite_defense._update()
        self.sprite_charge._update()
        
        self.sprite_spell._update()
        
        self.sprite_spell_dragon._update()
        
    def render(self, screen):
        #character
        if(self.sprite_attack.is_playing()):
            self.sprite_attack._render(screen, (Consts.CHARACTER_POSITION[0]-30,Consts.CHARACTER_POSITION[1]-130))
        else:
            self.sprite._render(screen, Consts.CHARACTER_POSITION)
            
        if(self.sprite_defense.is_playing()):
            self.sprite_defense._render(screen, (Consts.CHARACTER_POSITION[0]-30,Consts.CHARACTER_POSITION[1]-30))
        if(self.sprite_charge.is_playing()):
            self.sprite_charge._render(screen, (Consts.CHARACTER_POSITION[0]-30,Consts.CHARACTER_POSITION[1]-30))
        
        
        if(self.sprite_spell.is_playing()):
            self.sprite_spell._render(screen, (Consts.DRAGON_POSITION[0]+15, Consts.DRAGON_POSITION[1]+60))
        
        if(self.sprite_spell_dragon.is_playing()):
            self.sprite_spell_dragon._render(screen, (Consts.CHARACTER_POSITION[0]-40,Consts.CHARACTER_POSITION[1]-50))
            
        #lifebar
        if(self.life>0):
            current_lifebar_rect = pygame.Rect(self.lifebar_rect)
            current_lifebar_rect.width = (self.life/self.FULL_LIFE)*self.lifebar_rect.width
            pygame.draw.rect(screen, Consts.GREEN_COLOR, current_lifebar_rect)
        pygame.draw.rect(screen, Consts.WHITE_COLOR, self.lifebar_rect,2)
        
        
    def attack(self):
        self.sprite_attack._play(1)
        #self.sprite._play(1)
        
    def defense(self):
        self.sprite_defense._play(1)
            
    def spell(self):
        self.sprite_spell._play(1)
    
    def receive_spell(self):
        self.sprite_spell_dragon._play(1)
    
    def charge(self):
        self.charged *=2
        self.sprite_charge._play(1)
        
    def unCharge(self):
        load = self.charged
        self.charged = 1
        return load
        
    def beHitted(self, damage):
        if(damage>0):
            self.life -= damage
        self.counter+=1
        print(str(self.counter)+" "+str(damage))
            
    def isDead(self):
        if(self.life<1):
            return True
        return False
    
    def reset(self):
        self.life = self.FULL_LIFE
        self.charged = 1