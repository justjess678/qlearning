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
    
myFile = open("labyrinth.txt","r")
lab=myFile.read()
print("Our Labyrinth:")
print(lab)
"get number of lines/rows & columns: LABYRINTH MUST BE SQUARE"
cols=rows=len(lab.splitlines())
"couts des actions"
step=-1
stepTrap=-20
stepExit=200
stepWall=-5
nbMaxSteps=5000   #nombre maximum de dpelacememtns autorises
penalty=0  #long term penalty
position=[0, 9] #starting position, top left
"matrix map of the maze"
lab=lab.splitlines()
maze=[]
for i in range(rows):
    maze.append([0]*(cols))
for y in range (rows):
    for x in range (cols):
        maze[y][x]=lab[y][x]

"possible moves from current position"
moves=[]
if (position[0]!=0):
    moves.append(Direction.left)
if (position[0]!=cols-1):
    moves.append(Direction.right)
if (position[1]!=0):
    moves.append(Direction.down)
if (position[1]!=rows-1):
    moves.append(Direction.up)
    
"move"
dest=[]
d=Direction.up
if d in moves:
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
        penalty+=stepTrap
        position=dest
    if(maze[dest[0]][dest[1]]=='0'): #wall
        penalty+=stepWall #stays in same position as before
    if(maze[dest[0]][dest[1]]=='5'): #exit
        penalty+=stepExit
        position=dest
    if(maze[dest[0]][dest[1]]=='1'): #trap
        penalty+=step
        position=dest

print(dest)