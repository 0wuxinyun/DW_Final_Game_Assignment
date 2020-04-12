'''
main file of game Kumamon_Run_Run_Run
'''

from GUI import MyGame
from kivy.app import App



class Kumamon_Run_Run_RunApp(App):
    def build(self):
        return MyGame()

Kumamon_Run_Run_RunApp().run()
