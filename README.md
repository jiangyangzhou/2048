# 2048
2048 in Python 2.7 with module Tkinter;   
It is writen by Jiang Yangzhou;   
It is writen in python2.7 with module Tkinter;    
    
I add a .cu version of 2048. I think it should run faster
#### Using guide of cu2048mtcl:
```
nvcc mt_2048.cu -o mt.exe   #for windows, 
                            #if linux, just similar, it should generate mt.out, and modify cu2048mtcl.py)
python2 cu2048mtcl.py
```
if it works fine, you can get result like this:  
![4096](https://github.com/jiangyangzhou/2048/blob/master/4096.JPG)  

if you want to call mt_2048.cu directly, you can do like this:
 ```
 .\mt.exe 1,2,3,4,1,2,3,4,4,3,2,1,0,0,0,0 1 1000 3
 #first arg is input 2048 blocks, 1 represent 2, 2 represent 4,  ....
 # second arg: if begin with 0: it will print detailed message, else it will not
 # third arg: experiment times for every case
 # forth arg: search depth
 ```
 
 
 
    
