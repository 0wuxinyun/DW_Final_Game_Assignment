from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import CoreLabel
from kivy.core.window import Window
from kivy.graphics import Color
import time 
import numpy as np
from libdw import sm


# catch function game end when police catch bear:
def catch(p1,p2):
    result=False
    xi=p1.pos[0]
    xf=p1.pos[0]+p1.size[0]
    yi=p1.pos[1]
    yf=p1.pos[1]+p1.size[1]

    
    if p2.pos[0] <= xf and p2.pos[0]>=xi and p2.pos[1]<=yf and p2.pos[1]>=yi:
        result=True

    if p2.pos[0]<=xf and p2.pos[0]>=xi and p2.pos[1]+p2.size[1]<=yf and p2.pos[1]+p2.size[1]>=yi:
        result=True
   
    if p2.pos[0]+p2.size[0]>=xi and p2.pos[0]+p2.size[0]<=xf and p2.pos[1]<=yf and p2.pos[1]>=yi:
        result=True

    if p2.pos[0]+p2.size[0]>=xi and p2.pos[0]+p2.size[0]<=xf and p2.pos[1]+p2.size[1]<=yf and p2.pos[1]+p2.size[1]>=yi:
        result=True
    return result



# Detect help function: wheather state trastate of not:
def dictect(p1,p2):
    result=False
    xi=p1[0][0]
    xf=p1[0][1]
    yi=p1[1][0]
    yf=p1[1][1]
    
    if p2.pos[0] <= xf and p2.pos[0]>=xi and p2.pos[1]<=yf and p2.pos[1]>=yi:
        result=True

    if p2.pos[0]<=xf and p2.pos[0]>=xi and p2.pos[1]+p2.size[1]<=yf and p2.pos[1]+p2.size[1]>=yi:
        result=True

    if p2.pos[0]+p2.size[0]>=xi and p2.pos[0]+p2.size[0]<=xf and p2.pos[1]<=yf and p2.pos[1]>=yi:
        result=True

    if p2.pos[0]+p2.size[0]>=xi and p2.pos[0]+p2.size[0]<=xf and p2.pos[1]+p2.size[1]<=yf and p2.pos[1]+p2.size[1]>=yi:
        result=True
    return result


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

class MyGame(Widget):
    def __init__(self,**kwargs):
        super(). __init__(**kwargs)
        ''' 
        Window.height=1400
        Window.width=2400

        '''
        Window.size = (1200, 1400)
        


        # request a keyboard object: 
        # a callback will be called when the keyboard has been closed [touch interface]
        self.key = Window.request_keyboard(self.key_closed,self)
        self.key.bind(on_key_down=self.key_down)
        self.speed = 15
        self.chance=3
        self.count = 10
        self.money=0
        self.timer=5
        self.Rewards_list=[]
        self.Wall_list=[]
        self.cd_list=[]
        self.catch=False
        self.catcher=[]
        self.end=False
        self.part_time=False
        self.asked=False
        self.cd_inf=None
        self.check_time=20
        self.count=2
        self.Color=(0, 1,0)
        # Polices' routes:
        '''
        3 polices
        '''
        # middle police 
        self.p1=Police()
        self.p1.start()
        self.Horizon_Route=((1030,1030),(680,1270))
        self.Horizon_Route_Direction=1

        # left police:
        self.p2=Police()
        self.p2.start()
        self.Cicle_Route=((200,660),(400,1200))
        self.Circle_Route_Direction=2

        # right police:
        self.p3=Police()
        self.p3.start()
        self.Check_Route=(None,None)
        self.Check_Route_Direction=0
        # Speed up chance:
        self.Speed_up_label=CoreLabel(text='Speed Up Chance: 3',font_size=20, bold=True)
        # default not draw force it to draw 
        self.Speed_up_label.refresh()
        
        # Money:
        self.Money_label=CoreLabel(text='Money: 0',font_size=20, bold=True)
        # default not draw force it to draw 
        self.Money_label.refresh()

         # Part time set:
        self.Cd_label = CoreLabel(text='Play CD in 5 second [Y/N]',font_size=20,bold=True)
        self.Cd_label.refresh()
        
        self.timer_label = CoreLabel(text='5 second',font_size=20,bold=True)
        self.timer_label.refresh()

        # Warning:
        self.Warning_label = CoreLabel(text='Safe',font_size=20,bold=True)
        self.Warning_label.refresh()
        # show the image: 


        Window.clearcolor = (1, 1, 1, 1)
        with self.canvas:
            

            # AGENTS:
            self.Play = Rectangle(pos=(0,0),size=(100,200),source='img/player.jpg')
            self.Police1 = Rectangle(pos=(1030,670),size=(100,200),source='img/police.jpg')
            self.Police2=Rectangle(pos=(200,400),size=(100,200),source='img/police.jpg')
            self.Police3=Rectangle(pos=(1750,850),size=(100,200),source='img/police.jpg')
            
           


            # Rewards: five rewards: 
            # middle 
            self.Reward1 = Rectangle(pos=(1030,950),size=(100,100),source='img/honey.png')
            self.Rewards_list.append(self.Reward1)
            # left side 
            self.Reward2 = Rectangle(pos=(200,400),size=(100,100),source='img/honey.png')
            self.Rewards_list.append(self.Reward2)
            self.Reward3 = Rectangle(pos=(660,400),size=(100,100),source='img/honey.png')
            self.Rewards_list.append(self.Reward3)
            self.Reward4 = Rectangle(pos=(660,1200),size=(100,100),source='img/honey.png')
            self.Rewards_list.append(self.Reward4)
            self.Reward5 = Rectangle(pos=(200,1200),size=(100,100),source='img/honey.png')
            self.Rewards_list.append(self.Reward5)
            # right side:
            self.cd1 = Rectangle(pos=(1750,400),size=(200,200),source='img/cd.jpeg')
            self.cd_list.append(self.cd1)
            self.cd2 = Rectangle(pos=(1750,1200),size=(200,200),source='img/cd.jpeg')
            self.cd_list.append(self.cd2)
            self.Reward6 = Rectangle(pos=(1700,900),size=(100,100),source='img/honey.png')
            self.Rewards_list.append(self.Reward6)
           
             
            # Walls :
            Color(0,0,0)
            self.Outv1=Rectangle(pos=(130,300),size=(20,1200))
            self.Outv2=Rectangle(pos=(2000,300),size=(20,1200))
            # self.Inv1=Rectangle(pos=(830,300),size=(20,1200))
            self.Inv11=Rectangle(pos=(830,300),size=(20,50))
            self.Inv12=Rectangle(pos=(830,600),size=(20,1200-300))
            # self.Inv2=Rectangle(pos=(1330,300),size=(20,1200))
            self.Inv21=Rectangle(pos=(1330,300),size=(20,50))
            self.Inv22=Rectangle(pos=(1330,600),size=(20,1200-300))
            #self.Inv3=Rectangle(pos=(1600,300),size=(20,350))
            self.Inv31=Rectangle(pos=(1600,300),size=(20,50))
            self.Inv32=Rectangle(pos=(1600,300+300),size=(20,350-300))
            # self.Inv4=Rectangle(pos=(1600,1130),size=(20,350))
            self.Inv41=Rectangle(pos=(1600,1130),size=(20,50))
            self.Inv42=Rectangle(pos=(1600,1130+300),size=(20,50))
            self.Outh1=Rectangle(pos=(130,1480),size=(1890,20))
            
            # self.Outh2=Rectangle(pos=(130,300),size=(1890,20))
            self.Outh21=Rectangle(pos=(130,300),size=(250,20))
            self.Outh22=Rectangle(pos=(130+450,300),size=(1890-250-200,20))
            # self.Inh1=Rectangle(pos=(830,650),size=(500,20))
            self.Inh11=Rectangle(pos=(830,650),size=(150,20))
            self.Inh12=Rectangle(pos=(830+350,650),size=(150,20))
            # self.Inh2=Rectangle(pos=(1600,650),size=(400,20))
            self.Inh21=Rectangle(pos=(1600,650),size=(100,20))
            self.Inh22=Rectangle(pos=(1600+300,650),size=(100,20))
            # self.Inh3=Rectangle(pos=(1600,1130),size=(400,20))
            self.Inh31=Rectangle(pos=(1600,1130),size=(100,20))
            self.Inh32=Rectangle(pos=(1600+300,1130),size=(100,20))
            self.Wall_list.append(self.Outv1)
            self.Wall_list.append(self.Outv2)
            self.Wall_list.append(self.Inv11)
            self.Wall_list.append(self.Inv12)
            self.Wall_list.append(self.Inv21)
            self.Wall_list.append(self.Inv22)
            self.Wall_list.append(self.Inv31)
            self.Wall_list.append(self.Inv41)
            self.Wall_list.append(self.Inv32)
            self.Wall_list.append(self.Inv42)
            self.Wall_list.append(self.Outh1)
            self.Wall_list.append(self.Outh21)
            self.Wall_list.append(self.Outh22)
            self.Wall_list.append(self.Inh11)
            self.Wall_list.append(self.Inh12)
            self.Wall_list.append(self.Inh21)
            self.Wall_list.append(self.Inh22)
            self.Wall_list.append(self.Inh31)
            self.Wall_list.append(self.Inh32)
        
             # LABEL
            self.Speed_up_label_on_canvas=Rectangle(texture=self.Speed_up_label.texture,pos=(2400-260,1400),size=(250,80))
            self.Money_label_on_canvas=Rectangle(texture=self.Money_label.texture,pos=(2400-160,1400-90),size=(150,80))
            self.Cd_label_on_canvas=Rectangle(texture=self.Cd_label.texture,pos=(10000,10000),size=(300,80))
            self.timer_label_on_canvas=Rectangle(texture=self.timer_label.texture,pos=(1000,10000),size=(300,80))
            
            Color(self.Color[0],self.Color[1],self.Color[2])
            self.Warning_label_on_canvas=Rectangle(texture=self.Warning_label.texture,pos=(2400-150,1400-90-90-90),size=(100,80))

        

        Clock.schedule_interval(self.police2_route,0)
        Clock.schedule_interval(self.police_route,0)
        Clock.schedule_interval(self.police3_route,0)
        Clock.schedule_interval(self.Part_time,0)
        Clock.schedule_interval(self.danger,0)
        Clock.schedule_interval(self.win,0)

    def win(self,dt):
        if (self.Money_label.text)=='Money: '+ str(6) and self.Play.pos[1]<300-60:
            self.Win_label()
            Clock.unschedule(self.police2_route)
            Clock.unschedule(self.police_route)
            Clock.unschedule(self.police3_route)

            
    def danger(self,dt):
        
        if self.catch:
            if self.end:
                self.End_label()
                Clock.unschedule(self.police2_route)
                Clock.unschedule(self.police_route)
                Clock.unschedule(self.police3_route)
                
            else:
                self.Warn_label()
                
            
        else:
            self.Safe_label()



    def key_closed(self):
        self.key.unbind(on_key_down=self.key_down)
        self.key=None
 
    def key_down(self,keyboard,keycode,text,modifiers):
        (x,y) =self.Play.pos
        curx=x
        cury=y
        if self.Cd_label_on_canvas.pos==(2400-310,1400-90-90) and (text=='y' or text=='n'):
            if text=='y':
                self.part_time=True
                self.canvas.remove(self.cd_inf)
                self.cd_list.remove(self.cd_inf)
                self.Cd_label_on_canvas.pos=(1000000,100000)
                
            else: 
                self.part_time=False
                self.Cd_label_on_canvas.pos=(1000000,100000)

        if self.chance>0 and text=='r':
            self.speed=50
            self.chance-=1
            self.Speed_up_label.text = 'Speed Up Chance: '+ str(self.chance)
            self.Speed_up_label.refresh()
            self.Speed_up_label_on_canvas.texture=self.Speed_up_label.texture
            
        if self.count>0 and self.speed==50:
            self.count-=1
        if self.count<=0 and self.speed==50:
            self.count=10
            self.speed=15
        # coord : up is positive / right is positive : bottom left is origin 
        move =True
        # cannot outbound

        if text == 'w':
            cury+=self.speed
        if text == 's':
            cury-=self.speed
        if text == 'a':
            curx-=self.speed
        if text == 'd':
            curx+=self.speed
           
        self.Play.pos=(curx,cury) 
        for wall in self.Wall_list:
            if catch(wall,self.Play):
                curx=x
                cury=y
                break 
        self.Play.pos=(curx,cury) 


        # Part Time:
        for cd in self.cd_list:
            if catch(self.Play,cd):
                if self.asked==0: 
                    self.Cd_label_on_canvas.pos=(2400-310,1400-90-90)
                    self.cd_inf=cd
                    self.asked=3
                    time.sleep(1)
                else: 
                    self.asked-=1
                

 
        # rewards? 
        for reward in self.Rewards_list:
            if catch(self.Play,reward):
                self.money+=1
                self.Money_label.text = 'Money: '+ str(self.money)
                self.Money_label.refresh()
                self.Money_label_on_canvas.texture=self.Money_label.texture
                self.canvas.remove(reward)
                self.Rewards_list.remove(reward)


        


                 
            

    def police_route(self,dt):
        
        (curx,cury) =self.Police1.pos
        self.p1.step((self.Police1,self.Play,self.Horizon_Route_Direction))
        x,y=self.Horizon_Route
        if self.p1.state == 'Route':
            speed=100*dt
            if self.Horizon_Route_Direction==1:
                cury+=speed
                if cury>=y[1]:
                    self.Horizon_Route_Direction=-1
            else:
                cury-=speed
                if cury<=y[0]: 
                    self.Horizon_Route_Direction=1

            
            self.Police1.pos=(curx,cury)
            if self.catch and 1 in self.catcher:
                if len(self.catcher)==1:
                    self.catch=False
                    self.catcher=[]
                else:
                    self.catcher.remove(1)
        if self.p1.state == 'Catch':
            self.catch=True
            self.catcher.append(1)
            self.catcher=list(set(self.catcher))
        if self.p1.state=='End':
            self.end=True

    def police2_route(self,dt):
        (curx,cury) =self.Police2.pos
        x,y=self.Cicle_Route
        self.p2.step((self.Police2,self.Play,self.Circle_Route_Direction))
        if self.p2.state == 'Route':
            speed=100*dt
            if self.Circle_Route_Direction==2:
                curx+=speed
                if curx>=x[1]:
                    self.Circle_Route_Direction=1
            if self.Circle_Route_Direction==1:
                cury+=speed
                if cury>=y[1]:
                    self.Circle_Route_Direction=-2
            if self.Circle_Route_Direction==-2:
                curx-=speed
                if curx<=x[0]:
                    self.Circle_Route_Direction=-1
            if self.Circle_Route_Direction==-1:
                cury-=speed
                if cury<=y[0]:
                    self.Circle_Route_Direction=2
            self.Police2.pos=(curx,cury)
            if self.catch and 2 in self.catcher:
                if len(self.catcher)==1:
                    self.catch=False
                    self.catcher=[]
                else:
                    self.catcher.remove(2)
        if self.p2.state == 'Catch':
            self.catch=True
            self.catcher.append(2)
            self.catcher=list(set(self.catcher))      
        

        if self.p2.state=='End':
            self.end=True


    def Part_time(self,dt):

        if self.part_time:
            self.timer_label_on_canvas.pos=(2400-310,1400-90-90)
            self.timer-=0.1
            self.timer_label.text = str(round(self.timer,0))+ ' seconds'
            self.timer_label.refresh()
            self.timer_label_on_canvas.texture=self.timer_label.texture
            if self.timer<=0:
                self.part_time=False
                self.timer=0
                self.timer_label_on_canvas.pos=(1000000,1000)
                # sounds
                # police come to check
                xf,yf=self.cd_inf.pos
                xi,yi=self.Police3.pos
                self.Check_Route=((xi,xf),(yi,yf))
                self.Check_Route_Direction=np.sign(yf-yi)
                if self.count!=0:
                    Clock.schedule_interval(self.police3_route,0)
                else:

                    self.count = 2


    def police3_route(self,dt):
        speed=50*dt
        (curx,cury) =self.Police3.pos
        x,y=self.Check_Route
        self.p3.step((self.Police3,self.Play,self.Check_Route_Direction))
        if self.p3.state == 'Route':
            if self.Check_Route_Direction==1:
                cury+=speed
                if cury>=y[1]:
                    self.Check_Route_Direction=0
                    self.count-=1
            elif self.Check_Route_Direction==-1:
                cury-=speed
                if cury<=y[1]: 
                    self.Check_Route_Direction=0
                    self.count-=1
            elif self.Check_Route_Direction==0 and self.check_time>=0:
                self.check_time-=0.025
            elif self.Check_Route_Direction==0 and self.check_time<0:
                xi,yi=self.Police3.pos
                xf,yf=(1750,850)
                self.Check_Route=((xi,xf),(yi,yf))
                self.Check_Route_Direction=np.sign(yf-yi)
                self.check_time=20
                
            self.Police3.pos=(curx,cury)
            if self.catch and 3 in self.catcher:
                if len(self.catcher)==1:
                    self.catch=False
                    self.catcher=[]
                else:
                    self.catcher.remove(3)
        if self.p3.state == 'Catch':
            self.catch=True
            self.catcher.append(3)
            self.catcher=list(set(self.catcher))

        if self.p3.state=='End':
            self.end=True    

    def Warn_label(self):
        self.canvas.remove(self.Warning_label_on_canvas)
        self.Warning_label.text = 'Warn'
        self.Warning_label.refresh()
        with self.canvas:
            Color(1,0,0)
            self.Warning_label_on_canvas=Rectangle(texture=self.Warning_label.texture,pos=(2400-150,1400-90-90-90),size=(100,80))
    
    def Safe_label(self):
        self.canvas.remove(self.Warning_label_on_canvas)
        self.Warning_label.text = 'Safe'
        self.Warning_label.refresh()
        with self.canvas:
            Color(0,1,0)
            self.Warning_label_on_canvas=Rectangle(texture=self.Warning_label.texture,pos=(2400-150,1400-90-90-90),size=(100,80))

    def End_label(self):
        self.canvas.remove(self.Warning_label_on_canvas)
        self.Warning_label.text = 'Game Over'
        self.Warning_label.refresh()
        with self.canvas:
            Color(0,0,1)
            self.Warning_label_on_canvas=Rectangle(texture=self.Warning_label.texture,pos=(800,600),size=(700,350))
        self.key.unbind(on_key_down=self.key_down)
        time.sleep(1)

    def Win_label(self):
        self.canvas.remove(self.Warning_label_on_canvas)
        self.Warning_label.text = 'Win!!!'
        self.Warning_label.refresh()
        with self.canvas:
            Color(0,0,1)
            self.Warning_label_on_canvas=Rectangle(texture=self.Warning_label.texture,pos=(800,600),size=(700,350))
        self.key.unbind(on_key_down=self.key_down)
        time.sleep(1)

class Kumamon_Run_Run_RunApp(App):
    def build(self):
        return MyGame()

Kumamon_Run_Run_RunApp().run()


