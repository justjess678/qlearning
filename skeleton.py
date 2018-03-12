# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 10:52:56 2018

@author: jess
"""

from enum import Enum
import numpy as np
from random import randrange
import string
import random

class Direction(Enum):
    up=0
    down=1
    left=2
    right=3
    
stepsTaken=0
nbMaxSteps=500
Q = {}
gamma=0.95
strat=1
epsilon=0.99
maze=[]
penalty=0
#values of each movement
step=-1
stepTrap=-20
stepExit=500
stepWall=-100
#current position of the robot
position=[0, 0]

#funciton that checks if a certain place in the Q matrix is empty, returns 1 if it is
def currentQEmpty():
    global Q
    global position
    moves=[]
    if (position[0]!=0):
        moves.append(Direction.left)
    if (position[0]!=cols-1):
        moves.append(Direction.right)
    if (position[1]!=0):
        moves.append(Direction.down)
    if (position[1]!=rows-1):
        moves.append(Direction.up)
    for d in moves:
        if (Q.get((position[0],position[1],d),'A')=='A'):
            return 1
    return 0
    
#intialise the Q matrix
cols=10
rows=10
values=np.zeros((rows,cols))
for x in range(rows):
        for y in range(cols):
            for dir in Direction:
                Q[(x, y, dir)] = 0
                
#fills the Q matrix (replaces empty values only)
def QFill(moves):
    global maze
    global position
    global Q
    global step
    global stepTrap
    global stepWall
    global stepExit
    global gamma
    for d in moves:
        reward=0
        newpos=position
        if d==Direction.up:
            newpos=[position[0], position[1]+1]
        if d==Direction.down:
            newpos=[position[0], position[1]-1]
        if d==Direction.left:
            newpos=[position[0]-1, position[1]]
        if d==Direction.right:
            newpos=[position[0]+1, position[1]]
        reward=reward+values[newpos[0],newpos[1]]
        if(Q.get((position[0],position[1],d),0)==0):
            Q[position[0],position[1],d]=reward
            
#Qmove: decides which move to make depending on current Q values
#this is where the issue is!
def Qmove(moves):
    global position
    global Q
    global step
    global stepTrap
    global stepWall
    global stepExit
    global gamma
    bestd=0
    newd=moves[random.randint(0,len(moves)-1)]
    for d in moves:
        newpos=position
        if d==Direction.up:
            newpos=[position[0], position[1]+1]
        if d==Direction.down:
            newpos=[position[0], position[1]-1]
        if d==Direction.left:
            newpos=[position[0]-1, position[1]]
        if d==Direction.right:
            newpos=[position[0]+1, position[1]]
        #update value to best value of new position
        if Q.get((newpos[0],newpos[1],d),0)>=Q.get((newpos[0],newpos[1],bestd),0):
            bestd=d
        Q[position[0],position[1],d]=Q.get((position[0],position[1],d),0)+ (values[newpos[0]][newpos[1]] + gamma * Q.get((newpos[0],newpos[1],bestd),1) - Q.get((position[0],position[1],d),0))      
        #update arrow
        if Q.get((position[0],position[1],d),0)>Q.get((position[0],position[1],newd),0):
            newd=d
    return newd
            
#create maze
ch=['0', '1', '3']
for i in range(cols):
    maze.append([0]*(cols))
    for j in range(cols):
        random_index = randrange(0,len(ch))
        maze[i][j]=ch[random_index]
        if i==cols-1 and j==cols-1:
            maze[i][j]='5'
        if i==0 and j==0:
            maze[i][j]='0'
        if(maze[i][j]=="1"):
            values[i][j]=step
        elif(maze[i][j]=="0"):
            values[i][j]=stepWall
        elif(maze[i][j]=="3"):
            values[i][j]=stepTrap
        else:
            values[i][j]=stepExit
#move
while(stepsTaken<nbMaxSteps):
    moves=[]
    #if he finishes he starts over
    if(position[0]==rows-1 and position[1]==cols-1):
        position[0]=0
        position[1]=0
        penalty=0
    #identify the moves he can legally make
    if (position[0]!=0):
        moves.append(Direction.left)
    if (position[0]!=cols-1):
        moves.append(Direction.right)
    d=moves[0]
    if (position[1]!=0):
        moves.append(Direction.down)
    if (position[1]!=rows-1):
        moves.append(Direction.up)
    dest=[]
    #choose epsilon value
    rand=random.uniform(0, 1)
    if(rand<epsilon**stepsTaken):
        strat=1
        #explore
    else:
        strat=2
        #exploit
    #print(epsilon**stepsTaken)
    if(currentQEmpty() or strat==1):
        QFill(moves)
        d=moves[random.randint(0,len(moves)-1)]#how and why he moves
        print('dumb')
    else:
        d=Qmove(moves)
        print('smart')
    if(d==Direction.left):
        dest.append(position[0]-1) #x decreases by 1 place
        dest.append(position[1]) #y does not change
    if(d==Direction.right):
        dest.append(position[0]+1) #x increases by 1 place
        dest.append(position[1]) #y does not change
    if(d==Direction.up):
        dest.append(position[0]) #x does not change&&
        dest.append(position[1]+1) #y increases by 1
    if(d==Direction.down):
        dest.append(position[0]) #x does not change
        dest.append(position[1]-1) #y decreases by 1
    #penalty is calculated
    penalty=penalty+values[dest[0]][dest[1]]
    if(maze[dest[0]][dest[1]]!='0'): #not a wall
        position=dest
    stepsTaken=stepsTaken+1
    #show Q matrix
    x=position[0]
    y=position[1]
    print("x:",x," y:",y)
    print(" UP:%s" % Q.get((x,y, Direction.up)))
    print(" DOWN:%s" % Q.get((x,y, Direction.down)))
    print(" LEFT:%s" % Q.get((x,y, Direction.left)))
    print(" RIGHT:%s\n" % Q.get((x,y, Direction.right)))