import time 
import numpy as np
from libdw import sm

from help_functions import catch,dictect


# class: State Machine of police:
# input is the position of police and Player  
'''
input is as the form of three tuple 
police
player
direction
'''

class Police(sm.SM):
    def __init__(self):
        self.start_state= 'Route'
        self.counter = 20
        self.mark=[]

    def get_next_state(self, state, inp):
        # check sournding:
        police = inp[0]
        play = inp[1]
        direction=inp[2]

        if state=='Route':
            
            # 1st : near ?
            xp,yp=police.pos
            wp,hp=police.size
            nearp=((xp-150,xp+150+wp),(yp-100,yp+100+hp))
            # route go go go:

            if dictect(nearp,play):
                # change state to catch !!!
                self.mark.append(police.pos)
                return 'Catch'


            # 2nd : see ?
            if direction==2:
                seep=((xp+wp,xp+200+wp),(yp,yp+hp))
            if direction==-2:
                seep=((xp-200,xp),(yp,yp+hp))
            if direction==1:
                seep=((xp,xp+wp),(yp+hp,yp+hp+200))
            if direction==-1:
                seep=((xp,xp+wp),(yp-200,yp))  
            if direction==0:
                seep=((xp-200,xp),(yp,yp+hp))
            if dictect(seep,play):
                # change to catch state:
                self.mark.append(police.pos)
                return 'Catch'
            return 'Route'
            
        if state=='Catch':

            if catch(police,play):
                return 'End'
            speed = 5
            dx= play.pos[0]-police.pos[0]
            dy= play.pos[1]-police.pos[1]
            if abs(dx) >= abs(dy):
                if dx>0:
                    police.pos=(police.pos[0]+speed,police.pos[1])
                else:
                    police.pos=(police.pos[0]-speed,police.pos[1])
            if abs(dx) < abs(dy):
                if dy>0:
                    police.pos=(police.pos[0],police.pos[1]+speed)
                else:
                    police.pos=(police.pos[0],police.pos[1]-speed)
        

            if self.counter>0:
                return 'Catch'
            else:
                origin = self.mark.pop
                dx= origin[0]-police.pos[0]
                dy= origin[1]-police.pos[1]
                while dx!=0 or dy!=0:
                    if dy!=0:
                        police.pos=(police.pos[0],police.pos[1]+np.sign(dy)*speed)
                    else:
                        police.pos=(police.pos[0]+np.sign(dx)*speed,police.pos[1])
                self.counter=20
                return 'Route'
        if state=='End':
            return 'End'

