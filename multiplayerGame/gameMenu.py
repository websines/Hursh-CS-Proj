import pygame

class Menu:
    def __init__(self):
        self.play = False
    
    def play(self):
        self.play = True

    def resume(self):
        self.inMenu = False
        # self.inMenu set to True if escape

    def update(self):
        # only if some action has taken place
        pass

    def drawMenu(self):
        # this will have different pages
        # main page... {resume, settings, quit, sound}
        # settings page... FOV, language(easter egg)
                # ban player (vote) # NOTE future feature
    
    def handleEvents(self):
        # mostly dealing with mouse motion...
        # arrow keys to select the menus...
        # by default stay on the resume button...
        pass

    def mainloop(self):
        while self.inMenu:
            self.handleEvents()
            self.update()
            self.draw()
        self.quit()

    def changeSettings(self,settings):
        # settings object to change the settings
        # learn how to reload the game after that
        pass

    def quit(self):
        # main.running will set to False
        pass
