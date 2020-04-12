import time 
import numpy as np


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




