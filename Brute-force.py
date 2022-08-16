import numpy as np
from dataclass import Data,batchImport
from skyclass import PSky

class bfsky(PSky):
    def __init__(self, dim, ps, radius, drange=[0,1000], wsize=300):
        """
        Initializer

        :param dim: int
            The dimension of data
        :param ps: int
            The occurance count of the instance.
        :param radius: int
            radius use to prevent data being pruned unexpectedly.
            Recommand to be set according to the name of .csv file.
        :param drange: list(int)
            data range [min, max]
        :param wsize: int
            Size of sliding window.
        """
        PSky.__init__(self, dim, ps, radius, drange, wsize)
    def receiveData(self, d):
        """
        Receive one new data.

        :param d: Data
            The received data
        """
        if len(self.window) >= self.wsize:
            del self.window[0]
            # print("del data")
        self.window.append(d)
        # print(self.window)
        
    def updateSkyline(self):
        pruned = self.window.copy() #for skyline 1
        # print("pruned is",pruned)
        
        clean = self.window.copy() #for skyline 2
        
        # print("clean is",clean)
        # pruning
        for d in self.window.copy():
            # Find the interval between income data and max range region
            if d in clean:    
                
                pastart = [self.drange[1] if i+2*self.radius+0.1>self.drange[1] 
                           else i+2*self.radius+0.1 for i in d]
                # print("in up-clean-pastart",pastart)
                pamax = [self.drange[1] for j in range(self.dim)]
                # print("in up-clean-pamax",pamax)
                                
                for p in clean.copy():
                    tag =0
                    for l in range(len(p)):
                        if p[l] > pastart[l] : #每一個維度都去進行比較全部都比較大才可以刪掉
                            # print("pl is", p[l])
                            # print("pstartl",pastart[l])
                            tag=tag+1
                        else:
                            continue
                    if tag == len(p):
                        clean.remove(p)
                    else:
                        continue
        
        for d in clean:
            pruned.remove(d)
        
        for d in pruned.copy():
            if d in pruned:
                pastart = [self.drange[1] if i+2*self.radius+0.1>self.drange[1] 
                           else i+2*self.radius+0.1 for i in d]
                pamax = [self.drange[1] for j in range(self.dim)]
                # prune data points that are obviously dominated by current data point

                for p in clean.copy():
                    tag2 =0
                    for l in range(len(p)):
                        if p[l] > pastart[l] : #每一個維度都去進行比較全部都比較大才可以刪掉
                            # print("pl is", p[l])
                            # print("pstartl",pastart[l])
                            tag2=tag2+1
                        else:
                            continue
                    if tag2 == len(p):
                        clean.remove(p)
                    else:
                        continue
        
        
        
        self.skyline = clean
        self.skyline2 = pruned
        # print("self.windows",self.window)
        # print("self.skyline is",self.skyline)
        # print("self.skyline2 is",self.skyline2)
    

def gravity(cgarray,ps,dim):
    tg=[]
    for d in range(dim):
        tg.append(0)
        
    temp=0
    gravitylist=[]
    for k in range(100): #30 is the data count
        for i in range(ps): # ps is the possible instance
            tg=cgarray[temp+i]+tg

        tg=tg/ps # ps is the possible instance
        ltg=tg.tolist()
        gravitylist.append(ltg)
        tg=[]
        for d in range(dim):
            tg.append(0)
        temp= temp +ps # ps is the possible instance
        
    return gravitylist

if __name__ == '__main__':
    
    test = bfsky(2, 5, 5, [0,1000], wsize=20)
    indata = batchImport('100_dim2_pos5_rad5_01000.csv',test.ps)
    inputlist = indata[0]
    inputarray = indata[1]#location for
    glist=gravity(inputarray,test.ps,test.dim)# turn uncertain data into certain data

    # print("glist0 type",type(glist[0]))
    
    for i in range(100):
        test.receiveData(glist[i])
        
        test.updateSkyline()
        print("test.getWindow()",test.getWindow())
        print("test.getSkyline()",test.getSkyline())
        