#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 16:06:17 2018

@author: pierre
"""
"""
piege = 3
case libre = 1
mur = 0

sortie = 5

"""

monFichier = open("Labyrinth.txt","r")
laby = monFichier.read()
liste=laby.split()

Plan=[]
j=0
a=0
while j<10:
    i=0
    liste2=[]
    while i<10:
        
        u=i+a
        liste2.append(liste[u])
        i=i+1
        
    Plan.append(liste2)
    j=j+1
    a=a+10 
    
print(Plan) 





