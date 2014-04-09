import sys
import pygame

class InputManager(object):

    def __init__(self):
        self._observers = []
    
    def update(self):
        for event in pygame.event.get():
            #Quit system
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            self.notify(event)
        
    def attach(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, event):
        for observer in self._observers:
            observer.receiveInput(event)