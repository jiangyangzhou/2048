# -*- coding: cp936 -*-
from Tkinter import *
from random import randrange
from tkMessageBox import *
from time import sleep
from threading import Thread
import winsound

class _2048:
    def __init__(self):
        self.block=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.blockMovement=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.b=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.root=Tk()
        self.a=Label(self.root,text='2048')
        self.a.pack()
        self.c=Canvas(height=350,width=320,bg='white')
        self.c.pack()
        self.f=Frame(self.root,width=300,height=300)
        self.f.place(x=30,y=50)
        self.Rec=self.c.create_rectangle(10,10,310,310,fill='lightgrey',outline='gray')
        self.grade=self.c.create_text(50,330,text="score:")
        self.thr=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.wax=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.flagMove=1
        self.newblock=(0,0)
        self.num=0
        for i in range(4):
            for j in range(4):
                self.b[i][j]=Button(self.f,bg='gray',width=8,height=3,state='disabled')
                self.b[i][j].grid(row=i,column=j)

        
        
    def getNewBlock(self):
        i= randrange(0,4)
        j=randrange(0,4)
        p=randrange(0,10)
        while self.block[i][j]!=0:
             i=randrange(0,4)
             j=randrange(0,4)         
        if p==0:
            self.block[i][j]=4
        else:
            self.block[i][j]=2
        self.newblock=(i,j)
        self.flagMove=0
        self.thr[i][j]=Thread(target=self.spark,args=(i,j))
        self.thr[i][j].start()

    def playMusic(self):
        #winsound.PlaySound('2.wax', winsound.SND_FILENAME)
        print '\a'
        
    def spark(self,i,j):
        for t in range(3):
            self.b[i][j]['width']=3*t+2
            self.b[i][j]['height']=t+1
            self.c.pack()
            sleep(0.06)
            
    def myThread(self,i,j):
        if not type(self.wax[i][j])==int and not self.wax[i][j].isAlive():
            self.wax[i][j]=Thread(target=self.playMusic)
            self.wax[i][j].start()
        if not type(self.thr[i][j])==int and not self.thr[i][j].isAlive():
            self.thr[i][j]=Thread(target=self.spark,args=(i,j))
            self.thr[i][j].start()
            
    def combineLeft(self):
       flag=1
       while flag==1:
             flag=0
             for i in range(4):
                 for j in range(3):
                     if self.block[i][j+1]!=0 and self.block[i][j]==0:
                        flag=1
                        self.flagMove=1
                        k=j
                        while k<3:
                              self.block[i][k]=self.block[i][k+1]
                              k=k+1
                        self.block[i][3]=0
       self.display()
       self.c.pack()
       sleep(0.01)                 
       for i in range(4):
            for j in range(3):
                if self.block[i][j]!=0 and self.block[i][j]==self.block[i][j+1]:
                   self.block[i][j]*=2
                   self.myThread(i,j)
                   k=j+1
                   self.flagMove=1
                   while k<3:
                         self.block[i][k]=self.block[i][k+1]
                         k=k+1
                   self.block[i][3]=0
                   
    def combineRight(self):
        flag=1
        while flag==1:
             flag=0
             for i in range(4):
                 for j in range(3):
                     if self.block[i][2-j]!=0 and self.block[i][3-j]==0:
                        flag=1
                        self.flagMove=1
                        k=3-j
                        while k>0:
                              self.block[i][k]=self.block[i][k-1]
                              k=k-1
                        self.block[i][0]=0
        self.display()
        self.c.pack()
        sleep(0.01)
        for i in range(4):
            for j in range(3):
                if self.block[i][3-j]!=0 and self.block[i][3-j]==self.block[i][2-j]:
                   self.block[i][3-j]*=2
                   self.myThread(i,j)
                   k=2-j
                   self.flagMove=1
                   while k>0:
                         self.block[i][k]=self.block[i][k-1]
                         k=k-1
                   self.block[i][0]=0
                   
    def combineUp(self):
       flag=1
       while flag==1:
            flag=0
            for j in range(4):
                for i in range(3):
                    if self.block[i+1][j]!=0 and self.block[i][j]==0:
                       flag=1
                       self.flagMove=1
                       k=i
                       while k<3:
                             self.block[k][j]=self.block[k+1][j]
                             k=k+1
                       self.block[3][j]=0
       self.display()
       self.c.pack()
       sleep(0.01)                 
       for j in range(4):
           for i in range(3):
               if self.block[i][j]!=0 and self.block[i][j]==self.block[i+1][j]:
                  self.block[i][j]*=2
                  self.myThread(i,j)
                  k=i+1
                  self.flagMove=1
                  while k<3:
                        self.block[k][j]=self.block[k+1][j]
                        k=k+1
                  self.block[3][j]=0
                   
    def combineDown(self):
        flag=1
        while flag==1:
             flag=0
             for j in range(4):
                 for i in range(3):
                     if self.block[2-i][j]!=0 and self.block[3-i][j]==0:
                        flag=1
                        self.flagMove=1
                        k=3-i
                        while k>0:
                              self.block[k][j]=self.block[k-1][j]
                              k=k-1
                        self.block[0][j]=0
        self.display()
        self.c.pack()
        sleep(0.01)                
        for j in range(4):
            for i in range(3):
                if self.block[3-i][j]!=0 and self.block[3-i][j]==self.block[2-i][j]:
                   self.block[3-i][j]*=2
                   self.myThread(3-i,j)
                   k=2-i
                   self.flagMove=1
                   while k>0:
                         self.block[k][j]=self.block[k-1][j]
                         k=k-1
                   self.block[0][j]=0
                   
    def getBlock(self):
        return self.block
    
    def judgeOver(self):
        flagFill=1
        flagCombine=0
        for i in range(4):
            for j in range(4):
                if self.block[i][j]==0:
                   flagFill=0      
        if flagFill==1:
           for i in range(3):
               for j in range(3):
                   if self.block[i][j]==self.block[i][j+1] or self.block[i][j]==self.block[i+1][j]:
                      flagCombine=1
        if flagFill==1 and flagCombine==0:         
           showinfo("2048","Game Over!")
           
    def display(self):
        for i in range(4):
            for j in range(4):
                if self.block[i][j]== 0:
                   self.b[i][j]['text']=" "
                   self.b[i][j]['bg']='gray'
                elif self.block[i][j]==2 or self.block[i][j]==4:
                     self.b[i][j]['bg']='white'
                     self.b[i][j]['disabledforeground']='dimgray'
                elif self.block[i][j]== 8 or self.block[i][j]== 16:
                     self.b[i][j]['disabledforeground']='white'
                     self.b[i][j]['bg']='orange'
                elif self.block[i][j]==32 or self.block[i][j]==64:
                     self.b[i][j]['disabledforeground']='white'
                     self.b[i][j]['bg']='darkorange'
                elif self.block[i][j]==128 or self.block[i][j]==256:
                     self.b[i][j]['disabledforeground']='white'
                     self.b[i][j]['bg']='yellow'                           
                elif self.block[i][j]==512 or self.block[i][j]==1024:
                     self.b[i][j]['disabledforeground']='white'
                     self.b[i][j]['bg']='gold'
                elif self.block[i][j]>=2048:
                     self.b[i][j]['disabledforeground']='white'
                     self.b[i][j]['bg']='plum'
                if self.block[i][j]>0:
                   self.b[self.newblock[0]][self.newblock[1]]['width']=8
                   self.b[self.newblock[0]][self.newblock[1]]['height']=3
                   self.b[self.newblock[0]][self.newblock[1]]['bg']='WhiteSmoke'
                   self.b[i][j]['text']=self.block[i][j]                             
                
    def operate(self , event):
        if event.keysym=='Up':
            self.combineUp()
        elif event.keysym=='Down':
            self.combineDown()
        elif event.keysym=='Left':
            self.combineLeft()
        elif event.keysym=='Right':
            self.combineRight()
        self.judgeOver()
        self.c.pack()
        if self.flagMove==1:
           self.display()
           self.getNewBlock()     
           self.display()
         
    def getCanvas(self):
        return self.c
    
    def getRoot(self):
        return self.root

my2048=_2048()
c=my2048.getCanvas()
root=my2048.getRoot()
my2048.getNewBlock()
my2048.display()
c.bind('<Key>', my2048.operate)
c.focus_set()
#c.pack()
root.mainloop()

a=input()
             
    
        

                                                
