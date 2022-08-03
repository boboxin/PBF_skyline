from cgi import test
from ctypes import sizeof
import itertools
from turtle import width

import attr
import numpy as np
import validators as vlds

from gridclass import Grid 
from dataclass import Data,batchImport


def gravity(cgarray):
    
    tg=[0,0]
    temp=0
    gravitylist=[]
    for k in range(30): #30 is the data count
        for i in range(5): # 5 is the possible instance
            tg=cgarray[temp+i]+tg

        tg=tg/5 # 5 is the possible instance
        gravitylist.append(tg)
        tg=[0,0]
        temp= temp +5 # 5 is the possible instance
    garray = np.array(gravitylist)# use array data type to return
                
    for h in range(30): 
        print(gravitylist[h])
    return garray

if __name__ == '__main__':
    # Npoints = 10
    # # Ncentres = 2
    # dim = 2
    # Lbox = 10.0

    
    # data = np.random.randint(0, Lbox, size=(Npoints, dim))
    
    # k=1
    # shape=(3,5,4,2)
    # for i in shape:
    #     print(k)
    #     k=i*k
    # arr = np.arange(k).reshape(shape)
    # print(data)
    # print("No. of dimensions: ", data.ndim)
    # test=Grid(data,3)
    # size= test.size
    # id=test.cell_id(data)
    # width=test.cell_width
    # print("size:",size)
    # print("id:",id)
    # print("width:",width)
    # print("--------------")
    indata = batchImport('30_dim2_pos5_rad5_01000.csv',5)
    inputlist = indata[0]
    inputarray = indata[1]#location for
    garray=gravity(inputarray)#
    # print("dimention of the garray=",garray.ndim)
    test = Grid(garray,3)#index
    print("grid size=" ,test.size)
    print("grid dim=",test.dim)
    print("grid edge=",test.edges)
    print("grid id=",test.cell_id(garray))
    print("-----------")
    
    # for i in range(30):
        
    #     # local = indata.getLocation(i)
    #     # minmaxtuple = inputlist[i].getMinMaxTuple()
    #     print("inputlist is :",inputlist[i])
    #     # print("locations is :", local)