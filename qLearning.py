# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 16:03:43 2018

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

class Strategie(Enum):
    Exploration=1;
    Exploitation=2
    
class Square(Enum):
    Trap=3
    Wall=0
    Free=1
    Exit=5
    
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
nbMaxSteps=20   #nombre maximum de dpelacememtns autorises
stepsTaken=0
penalty=0  #long term penalty
position=[0, 0] #starting position, top left
Q=[]
gamma=0.95
robotID=0
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
        if (position[1]!=0):
            moves.append(Direction.down)
        if (position[1]!=rows-1):
            moves.append(Direction.up)
        dest=[]
        d=moves[random.randint(0,len(moves)-1)]#how and why he moves
        QFill(maze,moves)
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
        penalty=penalty+values[dest[0]][dest[1]]
        if(maze[dest[0]][dest[1]]!='0'): #wall
            position=dest
        top.after(500, updateRobotPos(dest))
        stepsTaken=stepsTaken+1
        print(dest)
        return(dest)
        
def updateRobotPos(dest):
    global position
    global C
    global lab
    global values
    buildMaze(lab, C, values)
    C.create_oval(0+dest[0]*40, 0+dest[1]*40, 40+dest[0]*40, 40+dest[1]*40, fill="yellow")
    
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
        reward=reward+values[position[0],position[1]]
        state=[position[0],position[1],d]
        Q[position[0]][position[1]]={'state':state,'reward':reward }
    #new_q = qsa + (values[position[0]][position[1]] + gamma * max(q[next_state, :]) - qsa)
    
def showQ():
    for x in range (cols):
        for y in range (rows):
            print(Q[x][y])
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
            maze[y][x]=lab[y][x]
            if(maze[y][x]=="1"):
                myColor="white"
                values[y][x]=step
            elif(maze[y][x]=="0"):
                myColor="black"
                values[y][x]=stepWall
            elif(maze[y][x]=="3"):
                myColor="red"
                values[y][x]=stepTrap
            else:
                myColor="green"
                values[y][x]=stepExit
            C.create_polygon(x*40, y*40, x*40+40, y*40, x*40+40 ,y*40+40, x*40, y*40+40, fill=myColor)
    #robotID=drawRobot(C,20,20,20)
    return maze

def drawRobot(canv,x,y,rad):
    # changed this to return the ID
    return canv.create_oval(x-rad,y-rad,x+rad,y+rad,width=0,fill='yellow')
    
myFile = open("labyrinth.txt","r")
lab=myFile.read()
print("Our Labyrinth:")
print(lab)
"get number of lines/rows & columns: LABYRINTH MUST BE SQUARE"
cols=rows=len(lab.splitlines())
for i in range(rows):
    Q.append([0]*(cols))
"matrix map of the maze"
lab=lab.splitlines()
values=np.zeros((rows,cols))
C = Canvas(top, bg = "white", height = rows*40, width = cols*40)
maze=buildMaze(lab, C, values)
C.pack()

d=Direction.up    
"move"
while(stepsTaken<nbMaxSteps):
    move(maze)
    top.update()
top.mainloop()
showQ()
