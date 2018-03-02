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
from tkinter import ttk, Tk, Toplevel
import welcome_support
from enum import Enum
import numpy as np
from random import randrange
import os

class Strategie(Enum):
    Exploration=1;
    Exploitation=2
    
class Direction(Enum):
    up=0
    down=1
    left=2
    right=3
directions=[Direction.up, Direction.down, Direction.left, Direction.right]

"couts des actions"
step=-1
stepTrap=-20
stepExit=500
stepWall=-100
nbMaxSteps=500   #nombre maximum de dpelacememtns autorises
stepsTaken=0
penalty=0  #long term penalty
position=[0, 0] #starting position, top left
Q = {}
gamma=0.95
robotID=0
"strategies"
"=1 -> exploration, =2 ->exploitation"
strat=1
epsilon=0.99
"GUI"
"build the output window"
top = Tk()
font10 = "-family Lato -size 16 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"
font11 = "-family Lato -size 14 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"
font12 = "-family Lato -size 18 -weight normal -slant roman "  \
    "-underline 0 -overstrike 0"
font14 = "-family Lato -size 12 -weight normal -slant roman "  \
    "-underline 0 -overstrike 0"
font9 = "-family Laksaman -size 24 -weight bold -slant roman "  \
    "-underline 0 -overstrike 0"
welcome_window = Toplevel(top)
welcome_window.title('Q-learning Labyrinth')
welcome_window.geometry("600x450+750+161")
usr=tkinter.IntVar()
usr.set(1)
mySize=tkinter.StringVar()
mySize.set('10')
myPath = StringVar()
myPath.set("labyrinth.txt")
lab_window = Toplevel(top)
lab_window.title('Labyrinth Solver')

top.withdraw() # hide top window
lab_window.withdraw() # hide lab window

def goto_lab():
    global usr
    welcome_window.withdraw()
    welcome_window.destroy()
    lab_window.deiconify() # show lab window
    runLab(usr.get(),int(mySize.get()),myPath.get())

butGo = ttk.Button(welcome_window, \
                     command=goto_lab)
#butGo.configure(foreground="#7bd93b")
#butGo.configure(font=font12)
butGo.configure(text='''Go!''')
butGo.place(relx=0.48, rely=0.84, height=41, width=65)

Title = Label(welcome_window)
Title.configure(text='''Q-Learning Labyrinth''')
Title.configure(foreground="#b30000")
Title.configure(font=font9)
Title.place(relx=0.25, rely=0.04, height=67, width=326)

filepath = Entry(welcome_window, textvariable=myPath)
filepath.place(relx=0.63, rely=0.4,height=30, relwidth=0.28)
filepath.configure(width=166)

pathLabel = Label(welcome_window)
pathLabel.place(relx=0.55, rely=0.4, height=27, width=47)
pathLabel.configure(font=font11)
pathLabel.configure(text='''Path:''')

Message1 = Message(welcome_window)
Message1.place(relx=0.57, rely=0.49, relheight=0.29, relwidth=0.33)
Message1.configure(text='''Files must be .txt types, with an equal number of rows and columns. '1' represents an empty square, '0' represents a wall, '3' represents a trap and '5' represents the exit. We recommend putting '5' at the bottom right and a '1' at the top left.''')
Message1.configure(width=200)

randomBut = Radiobutton(welcome_window, variable=usr, value=1)
randomBut.place(relx=0.08, rely=0.31, relheight=0.07, relwidth=0.36)
randomBut.configure(activebackground="#d9d9d9")
randomBut.configure(font=font10)
randomBut.configure(justify=LEFT)
randomBut.configure(text='''Random Labyrinth''')
        
udef = Radiobutton(welcome_window, variable=usr, value=2)
udef.place(relx=0.47, rely=0.31, relheight=0.07, relwidth=0.45)
udef.configure(activebackground="#d9d9d9")
udef.configure(font=font10)
udef.configure(justify=LEFT)
udef.configure(text='''User-defined Labyrinth''')

Spinbox1 = Spinbox(welcome_window, from_=1.0, to=100.0, textvariable=mySize)
Spinbox1.place(relx=0.32, rely=0.4, relheight=0.06, relwidth=0.08)
Spinbox1.configure(activebackground="#f9f9f9")
Spinbox1.configure(background="white")
Spinbox1.configure(font=font14)
Spinbox1.configure(from_="1.0")
Spinbox1.configure(to="20.0")
Spinbox1.configure(width=50)

pathLabel1 = Label(welcome_window)
pathLabel1.place(relx=0.2, rely=0.4, height=27, width=47)
pathLabel1.configure(activebackground="#f9f9f9")
pathLabel1.configure(font=font11)
pathLabel1.configure(text='''Size:''')


    
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
            penalty=0
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
        top.after(1, updateRobotPos(position))
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
        if (Q.get((position[0],position[1],d),0)==0):
            return 1
    return 0
    
def initQ():
    global Q
    global rows
    for x in range(rows):
        for y in range(cols):
            for dir in Direction:
                Q[(x, y, dir)] = 0
nbvis=0   
def showQ():
    global nbvis
    x=position[0]
    y=position[1]
    if(nbvis==0):
        thefile = open('Q.txt', 'w')
    else:
        thefile = open('Q.txt', 'a')
    print(x," ",y)
    thefile.write("(%s, " % x)
    thefile.write("%s)"% y)
    print(" UP:%s" % Q.get((x,y, Direction.up)))
    print(" DOWN:%s" % Q.get((x,y, Direction.down)))
    print(" LEFT:%s" % Q.get((x,y, Direction.left)))
    print(" RIGHT:%s\n" % Q.get((x,y, Direction.right)))
    thefile.write(" UP:%s" % Q.get((x,y, Direction.up)))
    thefile.write(" DOWN:%s" % Q.get((x,y, Direction.down)))
    thefile.write(" LEFT:%s" % Q.get((x,y, Direction.left)))
    thefile.write(" RIGHT:%s\n" % Q.get((x,y, Direction.right)))
    print("\n")
    if(x==cols-1):
        thefile.write("\n****************************\n")    
        print("\n")
    nbvis=nbvis+1

def buildMaze(lab, C, values):
    global rows,cols,robot,directions
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
            C.create_polygon(x*40, y*40, x*40+41, y*40, x*40+41 ,y*40+41, x*40, y*40+41, fill=myColor)
            #get best direciton
            moves=[]
            if (x>=0):
                moves.append(Direction.left)
            if (x<cols):
                moves.append(Direction.right)
            if (y>=0):
                moves.append(Direction.down)
            if (y<rows):
                moves.append(Direction.up)
            bestd=moves[0]
            for d in moves:
                if(Q.get((x,y,d),-1000)>(Q.get((x,y,bestd),-1000))):
                    bestd=d                
            if (bestd==Direction.up):
                arrow="up"
            elif (bestd==Direction.down):
                arrow="down"
            elif (bestd==Direction.left):
                arrow="left"
            elif (bestd==Direction.right):
                arrow="right"
            if(Q.get((x,y,bestd),-1000)>-1 and Q.get((x,y,bestd),-1000)<=100):
                #lightest arrow
                arrow+="1.gif"
            elif(Q.get((x,y,bestd),-1000)>100 and Q.get((x,y,bestd),-1000)<=200):
                arrow+="2.gif"
            elif(Q.get((x,y,bestd),-1000)>200 and Q.get((x,y,bestd),-1000)<=300):
                arrow+="3.gif"
            elif(Q.get((x,y,bestd),-1000)>300 and Q.get((x,y,bestd),-1000)<=400):
                arrow+="4.gif"
            elif(Q.get((x,y,bestd),-1000)>400):
                arrow+=".gif"
            elif(Q.get((x,y,bestd),-1000)<=-1 or Q.get((x,y,bestd),-1000)==0 or Q.get((x,y,bestd),-1000)==-1000):
                arrow=0
            if(arrow!=0 and maze[x][y]=="1"):
                #show arrow
                img = tkinter.PhotoImage(file=arrow)
                arrowPic = Label(image=img)
                arrowPic.image = img # keep a reference!
                C.create_image((x*40,y*40),image=img,anchor='nw')
                
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
    rmaze[0][0]='1'
    return rmaze
    
def runLab(userChoice=1, size=10, path='labyrinth.txt'):
    global top, lab_window, values, C, rows, cols, lab
    if userChoice==2:
        myFile = open(path,"r")
        lab=myFile.read()
        "get number of lines/rows & columns: LABYRINTH MUST BE SQUARE"
        cols=rows=len(lab.splitlines())
        "matrix map of the maze"
        lab=lab.splitlines()
    elif userChoice==1:
        lab=randomMaze(size)
        cols=rows=size
    print("Our Labyrinth:")
    print(lab)
    initQ()
    values=np.zeros((rows,cols))
    C = Canvas(lab_window, bg = "white", height = rows*40, width = cols*40)
    maze=buildMaze(lab, C, values)
    C.pack()
    #move
    while(stepsTaken<nbMaxSteps):
        move(maze)
        top.update()
        showQ()
    #top.mainloop()

top.mainloop()
