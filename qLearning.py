# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 16:03:43 2018

Hand in 18 mars 23.55
pgimenez@irit.fr

@author: jess

Python version 3.5
"""

"""tk inter for GUI

Code:     mur=0
            piege=3
            libre=1
            sortie=5
"""
import string
import random
import tkinter
from tkinter import *
from enum import Enum
import numpy as np
from random import randrange

class Strategie(Enum):
    Exploration=1;
    Exploitation=2
    
class Direction(Enum):
    up=0
    down=1
    left=2
    right=3

"couts des actions"
step=-1
stepTrap=-20
stepExit=500
stepWall=-100
nbMaxSteps=500   #nombre maximum de dpelacememtns autorises
stepsTaken=0
penalty=0  #long term penalty
position=[0, 0] #starting position, top left
Q=[]
gamma=0.95
robotID=0
"strategies"
"=1 -> exploration, =2 ->exploitation"
strat=1
epsilon=0.99
"GUI"
"build the output window"
top = Tk()
    
def move(maze):
    global penalty
    global position
    global stepsTaken
    global rows
    global cols
    global robotID
    global top
    if(stepsTaken<nbMaxSteps):
        moves=[]
        #s"il finit, il revient au début
        if(position[0]==rows-1 and position[1]==cols-1):
            position[0]=0
            position[1]=0
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
        rand=random.uniform(0, 1)
        if(rand<epsilon**stepsTaken):
            strat=1
            #explore
        else:
            strat=2
            #exploit
        #print(epsilon**stepsTaken)
        if(currentQEmpty() or strat==1):
            QFill(maze,moves)
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
        top.after(50, updateRobotPos(position))
        stepsTaken=stepsTaken+1
        print(dest)
        return(dest)
        
def updateRobotPos(dest):
    global position
    global C
    global lab
    global values
    #not efficient AT ALL lol but it works
    buildMaze(lab, C, values)
    C.create_oval(0+position[0]*40, 0+position[1]*40, 40+position[0]*40, 40+position[1]*40, fill="yellow")
    
def QFill(maze,moves):
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
        state=(position[0],position[1],d)
        if(Q[position[0]][position[1]].get(state,0)==0):
            Q[position[0]][position[1]][state]=reward
        
def Qmove(moves):
    global position
    global Q
    global step
    global stepTrap
    global stepWall
    global stepExit
    global gamma
    bestd=0
    bestState=0
    for d in moves:
        reward=-1000
        newpos=position
        if d==Direction.up:
            newpos=[position[0], position[1]+1]
        if d==Direction.down:
            newpos=[position[0], position[1]-1]
        if d==Direction.left:
            newpos=[position[0]-1, position[1]]
        if d==Direction.right:
            newpos=[position[0]+1, position[1]]
        state=(newpos[0],newpos[1],d)
        #update value to better value
        if Q[newpos[0]][newpos[1]].get(state,-2000)>reward:
            bestd=d
            bestState=(newpos[0],newpos[1],bestd)
    #new_q = qsa + (values[newpos[0]][newppos[1]] + gamma * max(q[next_state, :]) - qsa)
    if (bestd!=0 and bestState!=0):
        bestState=state
        Q[newpos[0]][newpos[1]][state]=Q[position[0]][position[1]].get(state,0)+ (values[newpos[0]][newpos[1]] + gamma * Q[newpos[0]][newpos[1]].get(bestState,0) - Q[position[0]][position[1]].get(state,0))
        return bestd
    else:
        return moves[random.randint(0,len(moves)-1)]
    
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
        state=(position[0],position[1],d)
        if (Q[position[0]][position[1]].get(state,0)==0):
            return 1
    return 0
    
def showQ():
    for x in range (cols):
        for y in range (rows):
            print(Q[x][y])
            print("\t\t")
        print("\n")

def buildMaze(lab, C, values):
    global rows
    global cols
    global robot
    maze=[]
    for i in range(rows):
        maze.append([0]*(cols))
    for y in range (rows):
        for x in range (cols):
            maze[x][y]=lab[y][x]
            if(maze[x][y]=="1"):
                myColor="white"
                values[x][y]=step
            elif(maze[x][y]=="0"):
                myColor="black"
                values[x][y]=stepWall
            elif(maze[x][y]=="3"):
                myColor="red"
                values[x][y]=stepTrap
            else:
                myColor="green"
                values[x][y]=stepExit
            C.create_polygon(x*40, y*40, x*40+40, y*40, x*40+40 ,y*40+40, x*40, y*40+40, fill=myColor)
    #robotID=drawRobot(C,20,20,20)
    return maze

def drawRobot(canv,x,y,rad):
    # changed this to return the ID
    return canv.create_oval(x-rad,y-rad,x+rad,y+rad,width=0,fill='yellow')

def randomMaze(size):
    rmaze=[]
    ch=['0', '1', '3']
    for i in range(size):
        rmaze.append([0]*(size))
        for j in range(size):
            random_index = randrange(0,len(ch))
            rmaze[i][j]=ch[random_index]
    rmaze[size-1][size-1]='5'
    return rmaze
    
myFile = open("labyrinth.txt","r")
lab=myFile.read()
print("Our Labyrinth:")
print(lab)
"get number of lines/rows & columns: LABYRINTH MUST BE SQUARE"
cols=rows=len(lab.splitlines())
for i in range(rows):
    Q.append([{}]*(cols))
"matrix map of the maze"
lab=lab.splitlines()
values=np.zeros((rows,cols))
C = Canvas(top, bg = "white", height = rows*40, width = cols*40)
maze=buildMaze(lab, C, values)
C.pack()
d=Direction.up    
#move
while(stepsTaken<nbMaxSteps):
    move(maze)
    top.update()
top.mainloop()
showQ()
