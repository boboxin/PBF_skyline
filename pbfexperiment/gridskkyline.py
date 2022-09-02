import os, sys
sys.path.append(os.path.abspath(os.pardir))

from data.dataClass import Data, batchImport

import matplotlib.pyplot as plt
import numpy as np
import time
# import zCurve as z 
import gridindex as gsp



class gridSKy():
    def __init__(self , dim , wsize , tem_array,dqueue):
        """
        Initializer

        sliding window
        """
        self.window = np.empty((0, dim+2), int) # sliding window
        self.wsize = wsize # sliding window size
        self.tem_array = tem_array
        self.dqueue = dqueue
        self.window_time = 0
        
    def receiveData(self, d):
        """
        Receive one new data.

        :param d: Data
            The received data
        """
        self.window_time = self.window_time + 1
        if len(self.window) >= self.wsize:
            # self.updateIndex(self.window[0], 'remove')
            self.window = np.delete( self.window , 0, axis=0)
        if len(self.window) > 0:
            if self.window_time - self.window[0][1] > self.wsize :
                self.window = np.delete( self.window , 0, axis=0)
        self.window = np.append(self.window , [d] , axis=0)
        # self.updateIndex(d,'insert')
        

    def updateSkyline(self):
        pruned = self.window.copy()
        if len(self.window) > 1:    
            for j in range(len(self.window) -1):
                tag = 0
                for i in range (dim):
                    if self.tem_array[pruned[-1][1]][i] > self.tem_array[pruned[j][1]][i]:
                        tag = tag+1
                    else:
                        continue
                if tag == dim:
                    tag = 0
                    for i in range(ps):
                        temarray = np.empty(0, int)
                        for k in range(dim):
                            temarray = np.append(temarray , dqueue[pruned[-1][1]].__dict__['locations'][i][k])
                        temarray = np.array(temarray).reshape(1,dim)
                        test = gsp.Grid(temarray,n)
                        uncertainData = test.cell_id(temarray)
                        uncertainDataGrid = np.where( cell_array == uncertainData )
                        for k in range(dim):
                            if uncertainDataGrid[k][0]>self.tem_array[pruned[j][1]][k]:
                                tag = tag+1
                            else:
                                continue
                if tag == dim*ps:
                    self.window = np.delete( self.window , -1 , axis=0)
                else:
                    continue
            """del new data"""

            a = np.empty(0,int)
            for j in range(len(self.window) -1):
                tag = 0
                for i in range (dim):
                    if self.tem_array[pruned[-1][1]][i] < self.tem_array[pruned[j][1]][i]:
                        tag = tag+1
                    else:
                        continue
                if tag == dim:
                    tag = 0
                    for i in range(ps):
                        temarray = np.empty(0, int)
                        for k in range(dim):
                            temarray = np.append(temarray , dqueue[pruned[j][1]].__dict__['locations'][i][k])
                        temarray = np.array(temarray).reshape(1,dim)
                        test = gsp.Grid(temarray,n)
                        uncertainData = test.cell_id(temarray)
                        uncertainDataGrid = np.where( cell_array == uncertainData )
                        for k in range(dim):
                            if self.tem_array[pruned[-1][1]][k]<uncertainDataGrid[k][0]:
                                tag = tag+1
                            else:
                                continue
                if tag == dim*ps:
                    a = np.insert(a , 0 , j )
                else:
                    continue
            for j in range(len(a)):
                self.window = np.delete( self.window , a[j] , axis=0)
            """del old data"""
    def showSkyline(self,i):
        #figure show
        plt.subplot(5, 5, i+1 , aspect="equal")
        plt.title(i+1)
        plt.scatter(self.window[:, 2], self.window[:, 3], c="r", marker=".", s=5)
        plt.xlim(0,1000)
        plt.ylim(0,1000)
        #          x_axis_data,y_axis_data,color,       marker size
        
if __name__ == '__main__':

    """
    test code
    """
    count = 25
    dim = 2
    ps = 5
    n = 32
    wsize = 10
    

    dqueue = batchImport('25_dim2_pos5_rad5_01000.csv', ps)
    gravityarray = np.empty((0, dim), int)
    for i in range(count):
        testlist = dqueue[i].__dict__['locations']
        tem = np.empty(0 , int)
        for j in range(dim):  
            temp = 0
            for k in range(ps):
                temp = testlist[k][j] + temp
            tem = np.append(tem , int(temp/ps))
        gravityarray = np.append(gravityarray , [tem] , axis=0)
    data_number = np.arange(count)
    gravityarray = np.c_[ data_number , gravityarray]


    data = gravityarray[: , 1:dim+1]
    test = gsp.Grid(data,n)
    tmp_cellID_array = test.cell_id(data)
    grid_array = np.c_[ tmp_cellID_array , gravityarray]
    """ grid_array:[grid_cell_id , point number , dim0 , dim1...] """

    cell_array = np.arange( n**dim ).reshape(n,n)
    # print(cell_array)
    # Z_array = np.empty(0 , int)
    tem_array = np.empty((0, dim), int)
    for i in range (count):
        x = np.where( cell_array == tmp_cellID_array[i] )
        tem = np.empty(0 , int)
        for i in range(dim):
            tem = np.append(tem , int(x[i][0]))
        tem_array = np.append(tem_array , [tem] , axis=0)
        # code = z.interlace(int(tem[0]) , int(tem[1]) )
        # Z_array = np.append(Z_array , [code])
    # Z_array = np.c_[ Z_array , empty_array]
    # print(tem_array)
    """Z_array:[Z_order_id , point number , dim0 , dim1...]"""

    plt.figure(0, figsize=(7, 7))
    start_time = time.time()
    test = gridSKy(dim, wsize ,tem_array,dqueue)
    for i in range (count):
        test.receiveData(grid_array[i])
        test.updateSkyline()
        test.showSkyline(i)

    print("--- %s seconds ---" % (time.time() - start_time))


    plt.tight_layout()
    plt.show()



    

    


 