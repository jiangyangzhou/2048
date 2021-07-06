# 2048 Solver
2048 in Python 2/3 with module Tkinter;  
Solve 2048 with Monte Carlo method.
Monto-carlo Sover with cuda / c++ / pure python!

### Solver Method 
To solve a 2048 game, you don't need to design complex heuristic function, or design a complex reinforce algorithm. Only with monto-carlo method, 2048 AI can achieve 4096!  

#### Monto-carlo Method  
For every step, Choose Up/Down/Left/Right for next step, and run the game randomly for many times, and see which direction can get higher scores. That is Monto-carlo method.  
I first achieve Python version 2048 solver, however python is too slow, and I can only run 30 times for each turns. But Python version can achieve 2048 as well.  
I try cuda to accelerate my codes. And it can run 1000 times for 64(4x4x4, 3depth) cases, and it can achieve 4096.

#### Using guide of cu2048mtcl:
```
nvcc mt_2048.cu -o mt_cu.exe   #Compile .cu  MC test program
g++ mt_2048.cpp -o mt_cpp.exe   # Compile c++ MC test program
python cu2048mtcl.py 
```
if it works fine, you can get result like this (If you are lucky,):  
![4096](https://github.com/jiangyangzhou/2048/blob/master/4096.JPG)  

if you want to call mt_2048.cu directly, you can do like this:
 ```
 .\mt_cu.exe 1,2,3,4,1,2,3,4,4,3,2,1,0,0,0,0 1 1000 3
 #first arg is input 2048 blocks, 1 represent 2, 2 represent 4,  ....
 # second arg: if begin with 0: it will print detailed message, else it will not
 # third arg: experiment times for every case
 # forth arg: search depth
 ```
 c++ version is similar:
 ```
 .\mt_cpp.exe 1,2,3,4,1,2,3,4,4,3,2,1,0,0,0,0 1 1000 3
 ```
 #### Performance analysis
|Trials  |Pure Python (s) | C++ (s) | Cuda (s) |
 |------ |:--------------:|:-----:|:-------:|
 |3000   |43              |0.51  |  0.081  |
 |3000\*4^2|-             |2.28   |  0.162  |
 |3000\*4^3|-             |10.61   |  0.411  |
 Note that python version implement is different, might the algorithm itself is slower.
 My Handware: 　　
 CPU:Intel(R) Core(TM) i5-1035G1 CPU @ 1.00GHz   1.19 GHz　　
 GPU: Geforce MX350
 
 
 
 #### Acknowledge
 Thanks @guikarist for providing C++ version MC test. 
 
 
    
