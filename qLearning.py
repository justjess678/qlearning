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

class Strategie(Enum):
    Exploration=1;
    Exploitation=2
    
class Square(Enum):
    Trap=3
    Wall=0
    Free=1
    Exit=5
    
class Direction(Enum):
    up=1
    down=2
    left=3
    right=4

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
    
def move(maze):
    global penalty
    global position
    global stepsTaken
    global rows
    global cols
    if(stepsTaken<nbMaxSteps):
        moves=[]
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
            dest.append(position[0]) #x does not change
            dest.append(position[1]+1) #y increases by 1
        if(d==Direction.down):
            dest.append(position[0]) #x does not change
            dest.append(position[1]-1) #y decreases by 1
        if(maze[dest[0]][dest[1]]=='3'): #trap
            penalty=penalty+stepTrap
            position=dest
            print("trap")
        if(maze[dest[0]][dest[1]]=='0'): #wall
            penalty=penalty+stepWall #stays in same position as before
            print("wall")
        if(maze[dest[0]][dest[1]]=='5'): #exit
            penalty=penalty+stepExit
            position=dest
            print("exit")
        if(maze[dest[0]][dest[1]]=='1'): #trap
            penalty=step+penalty
            position=dest
        stepsTaken=stepsTaken+1
        print(dest)
        return(dest)
            
def QFill(maze,moves):
    global position
    global Q
    global step
    global stepTrap
    global stepWall
    global stepExit
    for d in moves:
        reward=0
        newpos=position
        if d==Direction.up:
            newpos=[position[0], position[1]+1]
        if d==Direction.down:
            newpos=[position[0], position[1]-1]
        if d==Direction.left:
            newpos=[position[0]-1, position[1]]
        if d==Direction.left:
            newpos=[position[0]+1, position[1]]
        if(maze[newpos[0]][newpos[1]]=='3'):
            "trap"
            reward=stepTrap
        elif(maze[newpos[0]][newpos[1]]=='0'):
            "wall"
            reward=stepWall
        elif(maze[newpos[0]][newpos[1]]=='5'):
            "exit"
            reward=stepExit
        elif(maze[newpos[0]][newpos[1]]=='1'):
            "nada"
            reward=step
        """need to implement the equation here"""
        p=[position[0],position[1],d]
        Q[position[0]][position[1]]={'desc':p,'reward':reward }
    
def showQ():
    print(Q)
    for x in range (cols):
        for y in range (rows):
            print(Q[x][y])
        print("\n")

def buildMaze(lab, C):
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
            elif(maze[y][x]=="0"):
                myColor="black"
            elif(maze[y][x]=="3"):
                myColor="red"
            else:
                myColor="green"
            C.create_polygon(x*40, y*40, x*40+40, y*40, x*40+40 ,y*40+40, x*40, y*40+40, fill=myColor)
    robot=C.create_oval(0, 0, 40, 40, fill="yellow")
    C.pack()
    return maze
    
myFile = open("labyrinth.txt","r")
lab=myFile.read()
print("Our Labyrinth:")
print(lab)
"get number of lines/rows & columns: LABYRINTH MUST BE SQUARE"
cols=rows=len(lab.splitlines())
for i in range(rows):
    Q.append([0]*(cols))
"GUI"
"build the output window"
top = Tk()
C = Canvas(top, bg = "white", height = rows*40, width = cols*40)
"matrix map of the maze"
lab=lab.splitlines()
maze=buildMaze(lab, C)
d=Direction.up    
"move"
while(stepsTaken<nbMaxSteps):
    move(maze)
top.mainloop()
showQ()
