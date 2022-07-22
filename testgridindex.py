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
    indata = batchImport('30_dim2_pos5_rad5_01000.csv',5)
    inputlist = indata[0]
    inputarray = indata[1]#location for
    print(inputarray)
    print("type of indata[1]=",type(inputarray))
    print("dimention of the indata[1]=",inputarray.ndim)
    test = Grid(inputarray,2)
    print("grid size=" ,test.size)
    print("grid dim=",test.dim)
    print("grid id=",test.cell_id(inputarray))
    print("-----------")
    
    for i in range(30):
        
        # local = indata.getLocation(i)
        # minmaxtuple = inputlist[i].getMinMaxTuple()
        print("inputlist is :",inputlist[i])
        # print("locations is :", local)