#States constants
import pygame

class Consts:
    #States
    STATE_CONTINUE    = 0
    STATE_ITEMS_BOARD = 1
    STATE_FIGHT       = 2
    
    #Colors
    WHITE_COLOR = pygame.Color(255,255,255)
    BLACK_COLOR = pygame.Color(0,0,0)
    RED_COLOR   = pygame.Color(255,0,0)
    HOVER_RED_COLOR   = pygame.Color(255,100,100)
    PRESSED_RED_COLOR   = pygame.Color(205,0,0)
    GREEN_COLOR = pygame.Color(0,255,0)
    GOLD_COLOR  = pygame.Color(225, 225, 10)
    LIGHT_GOLD_COLOR   = pygame.Color(220, 220, 125)
    HOVER_GOLD_COLOR   = pygame.Color(230, 230, 170)
    PRESSED_GOLD_COLOR = pygame.Color(200, 200, 130)
    GRAY_COLOR = pygame.Color(150,150,150)
    HOVER_GRAY_COLOR = pygame.Color(180,180,180)
    PRESSED_GRAY_COLOR = pygame.Color(120,120,120)
    

    #Images
    SWORD_IMAGE = pygame.image.load("images/sword.png")
    HELMET_IMAGE = pygame.image.load("images/helmet.png")
    ARMOR_IMAGE = pygame.image.load("images/armor.png")
    SPELL_BOOK_IMAGE = pygame.image.load("images/spell_book.png")
    
    FIGHT_BACKGROUND = "images/scenario.png"
    
    SPRITE_DEFENSE = "images/defense.png"
    SPRITE_CHARGE = "images/charge.png"
    
    CHARACTER_STILL = "images/guy_still.png"
    CHARACTER_ATTACK = "images/guy_attack.png"
    DRAGON_ATTACK = "images/dragon_attack.png"
    DRAGON_STILL = "images/dragon_still.png"
    
    SPELL_CHARACTER = "images/spell_guy.png"
    SPELL_DRAGON = "images/spell_dragon.png"
    
    
    #Item descriptions
    SWORD_DESCRIPTION = "Attack Damage"
    HELMET_DESCRIPTION = "Armor"
    ARMOR_DESCRIPTION = "Armour"
    SPELL_BOOK_DESCRIPTION = "Spell Damage"
    BUY = "Buy"
    PLAY = "P l a y"
    
    #Items price
    SWORD_PRICE = 1100;
    HELMET_PRICE = 700;
    ARMOR_PRICE = 1300;
    SPELL_PRICE = 2000;
    
    #Items bonus
    SWORD_BONUS = 4;
    HELMET_BONUS = 4;
    ARMOR_BONUS = 8;
    SPELL_BONUS = 8;
    
    #Sprites
    PLAY_INFINITY = -1
    
    
    #Postions
    CHARACTER_POSITION = (380,340)
    DRAGON_POSITION = (320,50)
    
    
    #Attacks
    ATTACK = 1
    DEFENSE = 2
    SPELL = 3
    CHARGE = 4