from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import CoreLabel
from kivy.core.window import Window



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







class MyWidget(Widget):
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
        self.speed = 50
        self.chance=3
        self.count = 10
        self.money=0
        self.Rewards_list=[]
        # Polices' routes:
        '''
        3 polices
        '''
        self.Horizon_Route=((200,800),(1000,1000))
        self.Horizon_Route_Direction=1
        # Speed up chance:
        self.Speed_up_label=CoreLabel(text='Speed Up Chance: 3',font_size=20, bold=True)
        # default not draw force it to draw 
        self.Speed_up_label.refresh()
        
        # Money:
        self.Money_label=CoreLabel(text='Money: 0',font_size=20, bold=True)
        # default not draw force it to draw 
        self.Money_label.refresh()

        # show the image: 
        with self.canvas:
            # AGENTS:
            self.Play = Rectangle(pos=(0,0),size=(100,200),source='img/player.jpg')
            self.Police = Rectangle(pos=(200,1000),size=(100,200),source='img/police.jpg')

            # OBJECTS: five objects 
            self.Reward1 = Rectangle(pos=(200,700),size=(100,100),source='img/honey.png')
            self.Rewards_list.append(self.Reward1)
            self.Reward2 = Rectangle(pos=(500,900),size=(100,100),source='img/honey.png')
            self.Rewards_list.append(self.Reward2)
            # LABEL
            self.Speed_up_label_on_canvas=Rectangle(texture=self.Speed_up_label.texture,pos=(2400-260,1400),size=(250,80))
            self.Money_label_on_canvas=Rectangle(texture=self.Money_label.texture,pos=(2400-160,1400-90),size=(150,80))

        Clock.schedule_interval(self.police_route,0)

    def key_closed(self):
        self.key.unbind(on_key_down=self.key_function)
        self.key=None
 
    def key_down(self,keyboard,keycode,text,modifiers):
        (curx,cury) =self.Play.pos
        if self.chance>0 and text=='r':
            self.speed=100
            self.chance-=1
            self.Speed_up_label.text = 'Speed Up Chance: '+ str(self.chance)
            self.Speed_up_label.refresh()
            self.Speed_up_label_on_canvas.texture=self.Speed_up_label.texture
            
        if self.count>0 and self.speed==100:
            self.count-=1
        if self.count<=0 and self.speed==100:
            self.count=10
            self.speed=50
        # coord : up is positive / right is positive : bottom left is origin 

        if text == 'w':
            cury+=self.speed
        if text == 's':
            cury-=self.speed
        if text == 'a':
            curx-=self.speed
        if text == 'd':
            curx+=self.speed
        self.Play.pos=(curx,cury) 
        
        # catch?
        if catch(self.Play,self.Police):
            print('Game Over')
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
        (curx,cury) =self.Police.pos
        x,y=self.Horizon_Route

        speed=100*dt
        if self.Horizon_Route_Direction!=0:
            curx+=speed
        else:
            curx-=speed
        if curx>=x[1]:
            self.Horizon_Route_Direction=0
        if curx<=x[0]:
            self.Horizon_Route_Direction=1
        self.Police.pos=(curx,cury)
        
  


class TryApp(App):
    def build(self):
        return MyWidget()

TryApp().run()
