try:
    import Tkinter as tk
except:
    import tkinter as tk
from random import randrange
try:
    from tkinter import messagebox
except:
    import Tkinter.tkMessageBox as messagebox
from threading import Thread
from multiprocessing import Pool
import ctypes
import os

class _2048Draw:
    def __init__(self,block,score):
        self.block = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        copyBlock(self.block,block)
        self.b = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.root = tk.Tk()
        self.a = tk.Label(self.root,text='2048')
        self.a.pack()
        self.c=tk.Canvas(height=350,width=320,bg='white')
        self.c.pack()
        self.f=tk.Frame(self.root,width=300,height=300)
        self.f.place(x=30,y=50)
        self.Rec=self.c.create_rectangle(10,10,310,310,fill='lightgrey',outline='gray')
        self.score=score      
        self.grade=self.c.create_text(50,330,text="score:"+ str(self.score))
        self.flagMove=1
        self.newblock=(0,0)
        self.num=0
        for i in range(4):
            for j in range(4):
                self.b[i][j]=tk.Button(self.f,bg='gray',width=8,height=3,state='disabled')
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
            self.score+=4
        else:
            self.block[i][j]=2
            self.score+=2
        self.newblock=(i,j)
        self.flagMove=0            
                   
    def getBlock(self):
        return self.block
           
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
                   self.b[i][j]['text']=self.block[i][j]
        self.c.delete(self.grade)
        self.grade=self.c.create_text(50,330,text="score:"+ str(self.score))
        self.c.update()
                
    def operate(self , event):
        flagMove=combine(self.block,event.keysym)
        self.judgeOver()
        self.c.pack()
        if flagMove>=1:
           self.getNewBlock()     
           self.display()

    def operate1(self, turn):
          flagMove=combine(self.block,turn)
          self.judgeOver()
          self.c.update()
          if flagMove==1:
               self.display()
               self.getNewBlock()
          self.display()
          #self.c.update()
         
    def getCanvas(self):
        return self.c
    
    def getRoot(self):       
        return self.root
    
    
    
class _2048operate:
    def __init__(self,block,score=0):
        self.block=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        copyBlock(self.block,block)
        self.score=score
                
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
            
    def judgeOver(self):
        flagFill=1
        flagCombine=0
        for i in range(4):
            for j in range(4):
                if self.block[i][j]==0:
                   flagFill=0      
        if flagFill==1:
            for i in range(4):
                 for j in range(4):
                      if (j<3 and self.block[i][j]==self.block[i][j+1] )or (i<3 and self.block[i][j]==self.block[i+1][j]):
                          flagCombine=1        
        if flagFill==1 and flagCombine==0:         
             return 0
        else:
              return 1
        
    def operate(self ,turn):
        flagMove=self.combine(turn)
        if flagMove>=1:
           self.getNewBlock()     
        return flagMove
           
           
    def blockRotate(self,turn):   
        temp = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        if turn=='along':
            for i in range(4):
                for j in range(4):
                    temp[i][j]=self.block[3-j][i]
        elif turn =='inverse':
            for i in range(4):
                for j in range(4):
                    temp[i][j]=self.block[j][3-i]
        for i in range(4):
            for j in range(4):
                self.block[i][j]=temp[i][j]    
                
    def combine(self,turn):      # 0:left,1:up,2:right,3:down
        if turn =='up' or turn =='Up' or turn==1:
            self.blockRotate('inverse')
        elif turn == 'right' or turn=='Right' or turn==2:
            self.blockRotate('along')
            self.blockRotate('along')
        elif turn== 'down' or turn=='Down' or turn==3:
            self.blockRotate('along')
        flag=1
        flagMove=0
        while flag==1:
            flag=0
            for i in range(4):
                for j in range(3):
                    if self.block[i][j+1]!=0 and self.block[i][j]==0:
                        flag=1
                        flagMove=1
                        k=j
                        while k<3:
                            self.block[i][k]=self.block[i][k+1]
                            k=k+1
                        self.block[i][3]=0         
        for i in range(4):
            for j in range(3):
                if self.block[i][j]!=0 and self.block[i][j]==self.block[i][j+1]:
                    self.block[i][j]*=2
                    self.block[i][j+1]=0
                    self.score+=self.block[i][j]
                    k=j+1
                    flagMove+=self.block[i][j]
                    while k<3:
                        self.block[i][k]=self.block[i][k+1]
                        k=k+1
                    self.block[i][3]=0   
        if turn =='up' or turn =='Up'or turn==1:
            self.blockRotate('along')
        elif turn == 'right' or turn=='Right'or turn==2:
            self.blockRotate('inverse')
            self.blockRotate('inverse')
        elif turn== 'down' or turn=='Down'or turn==3:
            self.blockRotate('inverse')  
        return flagMove
 
 
def copyBlock(myblock,block):     
    for i in range(4):
        for j in range(4):
            myblock[i][j]=block[i][j]       
    
def maxA(arr,length,layer):
    list=[]
    for j in range(layer):
        max=-100000000
        num=-1
        for i in range(length):
            if arr[i]>=max and not i in list:
                max=arr[i]
                num=i
        list.append(num)
    return list

def log2(num):
    i=1
    while num>2:
        num/=2
        i+=1
    return i   

class AI2048:
    def __init__(self,block):
        self.perlife=[0]*10
        self.block=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        copyBlock(self.block, block)
        
    def assess1(self,turn,k,m,n,l):
        tempgame=_2048operate(self.block)
        if tempgame.combine(turn)==0:
            assess=-10000000
        else:
            assess=k*self.numSpace()+ m*self.smooth()+ n*self.continuity()+10*tempgame.score
        return assess
    
    def numSpace(self):
        space=0
        for i in range(4):
            for j in range(4):
                if self.block[i][j]==0:
                    space+=1
        return space        
    
    def continuity(self):
        conScore=0
        for i in range(4):
            for j in  range(4):
                if j<3 and self.block[i][j]>self.block[i][j+1]:
                    conScore+=10*i*(3-j)
                else:
                    conScore-=10*i*(3-j)
                if i>0 and self.block[i][j]>self.block[i-1][j]:
                    conScore+=10
                else:
                    conScore-=10
        return conScore
            
    def smooth(self):
        smoothScore=0
        for i in range(4):
            for j in range(4):
                if self.block[i][j]==0:
                    continue
                else:
                    if i>0 and self.block[i-1][j]!=0:
                        smoothScore-=(log2(self.block[i][j])-log2(self.block[i-1][j]))**2
                    if i<3 and self.block[i+1][j]!=0:
                        smoothScore-=(log2(self.block[i][j])-log2(self.block[i+1][j]))**2
                    if j>0 and self.block[i][j-1]!=0:
                        smoothScore-=(log2(self.block[i][j])-log2(self.block[i][j-1]))**2
                    if j<3 and self.block[i][j+1]!=0:
                        smoothScore-=(log2(self.block[i][j])-log2(self.block[i][j+1]))**2          
        return smoothScore   
    
    def assess(self,k,m,n,l):
        assess=[0,0,0,0]
        for turn in range(4):
            assess[turn]=self.assess1(turn,k,m,n,l)    
        return maxA(assess, 4,1)[0]
        
    def tryMove(self,times):
        perlife=[0,0,0,0]
        avi=[]
        for turn in range(4):
            if self.assess1(turn,100,5,5,10)>-1000000:
                avi.append(turn)
        for turn in avi:
            for i in range(times):
                mygame=_2048operate(self.block,0)
                life=0
                mygame.operate(turn)
                while (mygame.judgeOver()==1):
                    d=randrange(0,4) 
                    flagMove=mygame.operate(d)
                    if flagMove>=1:
                        life+=1                 
                perlife[turn]+=life
        return maxA(perlife,4,1)[0]
    
    def threadTry(self,turn,j):
        life=[0]*100
        self.perlife[j]=0
        for i in range(30):
            mygame=_2048operate(self.block,0)
            life[i]=0
            mygame.operate(turn)
            while (mygame.judgeOver()==1):
                d=randrange(0,4) 
                mygame.operate(d)
                life[i]+=1    
            self.perlife[j]+=life[i]
        self.perlife[j]/=3
    


def mtcl2048(block):
    str=""
    dic2={0:0, 2:1,4:2,8:3,16:4,32:5,64:6,128:7,256:8,512:9,
            1024:10,2048:11,4096:12,8192:13}
    for i in range(16):
        str+="%d,"%dic2[block[i//4][i%4]]
    str = str[:-1]
    args = "mt.exe %s 1"%str
    result = os.system(args)
    print(args,"  ",result)
    #in .cu: 0:left, 1:down, 2:right, 3:up
    #in .py: 0:left, 1:up, 2:right, 3:down
    turn_list = [0,3,2,1]

    return turn_list[result]
       
    
def do():
    #lib = ctypes.cdll.LoadLibrary("mtcl2048.dll")
    block=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    score=0
    mygame=_2048operate(block,0)
    mygame.getNewBlock()
    mygame.getNewBlock()
    copyBlock(block,mygame.block)
    draw2048=_2048Draw(block,0)
    draw2048.display()
    while(mygame.judgeOver()==1):
        mygame=_2048operate(block,score)
        ai2048=AI2048(block)
        if ai2048.numSpace()>4 and score<10000:
            turn=ai2048.assess(100,5,5,10)
        else:
            #turn=ai2048.tryMove(50)
            turn = mtcl2048(block)
        mygame.operate(turn)
        copyBlock(block,mygame.block)
        copyBlock(draw2048.block,block)
        score=mygame.score
        draw2048.score=mygame.score
        draw2048.display()     
    messagebox.showinfo("2048","Game Over!"+str(score))


        
do()
