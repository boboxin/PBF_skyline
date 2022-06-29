from cgi import test
from ctypes import sizeof
import itertools
from turtle import width

import attr
import numpy as np
import validators as vlds

from gridclass import Grid 
from dataclass import Data,batchImport

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
    indata = batchImport('30_dim5_pos1_rad1_01000.csv',1)
    inputlist = indata[0]
    inputarray = indata[1]
    print(inputarray)
    print("type of indata=",type(inputarray))
    print("dimention of the indata=",inputarray.ndim)
    test = Grid(inputarray,2)
    print("size=" ,test.size)
    print("grid dim=",test.dim)
    print("id=",test.cell_id(inputarray))
    
    for i in range(30):
        # print("indata[",i,"]=",inputlist[i])
        # print("cindata[",i,"]=",cindata[i])
        
        # local = indata.getLocation(i)
        minmaxtuple = inputlist[i].getMinMaxTuple()
        print("tpl is :",minmaxtuple)
        # print("locations is :", local)