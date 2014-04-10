#class abstract for the states
from inputListener import InputListener

class State(InputListener):
    
    def __init__(self, screen, inputManager): 
        self.screen = screen
        self.inputManager = inputManager
        inputManager.attach(self)
        
    def destroy(self): pass
    
    def _update(self): return 0
    def _render(self): pass
        