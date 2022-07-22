import attr
import numpy as np
import validators as vlds

from gridclass import Grid 
from dataclass import Data,batchImport

if __name__ == '__main__':
    indata = batchImport('30_dim2_pos5_rad5_01000.csv',5)
    inputlist = indata[0]
    inputarray = indata[1]#location
    tg=[0,0]
    temp=0
    gravitylist=[]
    for k in range(30): #30 is the data count
        for i in range(5): # 5 is the possible instance
            tg=inputarray[temp+i]+tg

        tg=tg/5 # 5 is the possible instance
        gravitylist.append(tg)
        tg=[0,0]
        temp= temp +5 # 5 is the possible instance
    for h in range(30): 
        print(gravitylist[h])   