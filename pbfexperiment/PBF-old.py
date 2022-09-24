from itertools import count
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import time

here = os.path.dirname(os.path.abspath(__file__))
class PSky():
    def __init__(self, count ,dim, ps, radius, drange, wsize):
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
        self.count = count
        self.dim = dim # data dimension
        self.ps = ps # possible instance count
        self.radius = radius # radius of a data
        self.drange = drange # data range
        self.wsize = wsize # sliding window size
        self.window = [] # sliding window
        self.locationwindow =[] # for pbf location
        self.skyline = [] # 1st set skyline candidate
        self.skyline2 = [] # 2nd set skyline candidate
        self.outdated = [] # temporary storage for outdated data
        # p = index.Property()
        # p.dimension = dim
        # p.dat_extension = 'data'
        # p.idx_extension = 'index'
        # self.index = index.Index(str(dim)+'d_index',properties=p) # r-tree index
    def getlocationWindow(self):
        return self.locationwindow
    def getWindow(self):
        return self.window
    def getSkyline(self):
        """
        Get the 1st set of skyline candidate.
        """
        return self.skyline
    def getSkyline2(self):
        """
        Get the 2nd set of skyline candidate.
        """
        return self.skyline2
    def getOutdated(self):
        """
        Get current outdated data
        """
        return self.outdated

class Data():
    """Class use to store data information"""
    def __init__(self, name, ps):
        """
        Initializer

        :param name: string
            The name (or label) of the data
        :param ps: int
            Instance count of the data. 
        """
        self.name = name
        self.pprob = ps
        self.probs = []
        self.locations = []
        self.regionMax = []
        self.regionMin = []
    def __updateMinMax(self, loc):
        """
        For use inside the class only.
        Use to update the bounding region.

        :param loc: list(int)
            the new location instance which added to data object
        """
        if self.regionMax == []:
            self.regionMax = loc.copy()
        else:
            for i, lu in enumerate(loc):
                if self.regionMax[i] < lu:
                    self.regionMax[i] = lu
        if self.regionMin == []:
            self.regionMin = loc.copy()
        else:
            for j, lm in enumerate(loc):
                if self.regionMin[j] > lm:
                    self.regionMin[j] = lm
    def insertLocation(self, prob, location):
        """
        Insert a new instance of data object.

        :param prob: float
            the probability of the new coming instance.
        :param location: list(int)
            the location of the new coming instance.
        """
        self.probs.append(prob)
        self.locations.append(location)
        self.__updateMinMax(self.locations[-1])
    def getLabel(self):
        """
        Get the name(label) of the data object
        """
        return self.name
    def getPCount(self):
        """
        Get the total instance count of the data object
        """
        return self.pprob
    def getProbLocSet(self, index):
        """
        Get a list which contain the occurance probability and instance location according to given index.
        If the given index exceed, the function will return [None, []]

        :param index: int
            The index of location, according to insertion sequence.(0 to n-1)         
        """
        try:
            return [self.probs[index], self.locations[index]]
        except:
            return [None, []]
    def getProb(self, index):
        """
        Get the occurance probability of instance according to given index.
        If the given index exceed, the function will return None
        
        :param index: int
            The index of occurance probability, according to insertion sequence.(0 to n-1)         
        """
        try:
            return self.probs[index]
        except:
            return None
    def getLocation(self, index):
        """
        Get the instance location according to given index.
        If the given index exceed, the function will return an empty list.
        
        :param index: int
            The index of instance location, according to insertion sequence.(0 to n-1)         
        """
        try:
            return self.locations[index]
        except:
            return []
    def getLocationMax(self):
        """
        Get the list which contains the maximium value of data location for each dimension.    
        """
        return self.regionMax
    def getLocationMin(self):
        """
        Get the list which contains the minimium value of data location for each dimension.    
        """
        return self.regionMin
    def getMinMaxTuple(self):
        """
        Get the suple which contains the minimium and maximium value of data location for each dimension.
        This function is use with rtree.
        The format of the tuple is: (d1min, d2min,..., dnmin, d1max, d2max,..., dnmax)     
        """
        return tuple(self.regionMin+self.regionMax)
    
    # Override default function
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    def __str__(self):
        return str(self.__dict__)
    def __hash__(self):
        return hash(str(self.__dict__))

class pbfsky(PSky):
    def __init__(self, count,dim, ps, radius, drange=[0,1000], wsize=300):
        """
        Initializer
        :param count: int
            The number of data
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
        PSky.__init__(self,count, dim, ps, radius, drange, wsize)
    def receiveData(self, d,l):
        """
        Receive one new data.

        :param d: Data
            The received data
        :param l: location
            d is all information l is the location that for calculate dominate
        """
        if len(self.window) >= self.wsize:
            del self.window[0]
            
            del self.locationwindow[0]
          
        self.window.append(d)
        self.locationwindow.append(l)
        
        
    def updateSkyline(self):
        

        clean = [] #for skyline 1
        clean_location = []
        
        pruned = [] #for skyline 2 canditate
        pruned_location = []
        
        s2temp=[] #for skyline2
        deltemp=[]
        deltemp2=[]
        for c1 in range(len(self.locationwindow)):
            for c2 in range(0,len(self.locationwindow),1):
                tag1 = 0
                for op in range(self.ps):
                    for np in range(self.ps):
                        jumptag1 = 0
                        for d in range(self.dim):
                            if  self.locationwindow[c2][np][d] < self.locationwindow[c1][op][d]:
                                tag1=tag1+1
                            else:
                                jumptag1=jumptag1+1
                          
                if tag1 == self.ps*self.ps*self.dim:
                    deltemp.append(c1) 
                else:
                    continue   
        for dele in range(len(self.window)):
            if dele not in deltemp:
                clean.append(self.window[dele])
                clean_location.append(self.locationwindow[dele])
            else:
                # if it need to be del it will be the skyline2canditate so we could put those into prune
                pruned.append(self.window[dele])
                pruned_location.append(self.locationwindow[dele])
         
        for p1 in range(len(pruned_location)):
            for p2 in range(0,len(pruned_location),1):
                tag2 = 0
                for op2 in range(self.ps):
                    for np2 in range(self.ps):
                        jumptag2 = 0
                        for dd in range(self.dim):
                            if  pruned_location[p2][np2][dd] < pruned_location[p1][op2][dd]:
                                tag2=tag2+1
                            else:
                                jumptag2=jumptag2+1
                          
                if tag2 == self.ps*self.ps*self.dim:
                    deltemp2.append(p1) 
                else:
                    continue        
        
        for dele2 in range(len(pruned)):
            if dele2 not in deltemp2:
                s2temp.append(pruned[dele2])
            else:
                continue
        
        self.skyline = clean
        self.skyline2 = s2temp
        
        
    def showSkyline(self,ll,i):
        #figure show
        
        plt.subplot(5,5, i-80 , aspect="equal")
        plt.title(i-80)
        for p in range(ll):
            plt.scatter(self.skyline[p][0], self.skyline[p][1], c="r", marker=".", s=30)
        plt.xlim(0,1000)
        plt.ylim(0,1000)
        
def batchImport(csvfile, ps):
    """
    Import data objects using csv file.
    This function returns a list of data object.
    
    :param csvfile: srting
        the .csv file locate in data/ of this project
    :param ps: float
        instance count of an object
    """
    result = []
    locatlist = []
    mm=[]
    with open(here+'/data/'+csvfile, 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        for row in csv_reader:
            data = Data(row[0], ps)
            llist =[]
            for p in range(ps):
                # Some awful string manipulation to parse numbers
                data.insertLocation(float(row[2*p+1]), [int(float(i)) for i in row[2*p+2].strip(' []').split(',')])
                # print(local)
                
                
                locat = data.getLocation(p) # my add
                llist.append(locat) # my add
                
                # larray = np.array(locatlist)# use array data type to return
                # print(larray[p],type(larray),larray.shape)
            locatlist.append(llist)
            getmm = data.getMinMaxTuple() 
            mm.append(getmm)
            result.append(data) #all is in a list
            
    return result,locatlist


    
if __name__ == '__main__':
    
    tbsky = pbfsky(10000,2, 5, 5, [0,1000], wsize=300)
    indata = batchImport('10000_dim2_pos5_rad5_01000.csv',tbsky.ps)
    dqueue = indata[0] #turn inputlist to dqueue
    locatlist = indata[1] #location for
    
    start_time= time.time()
    for i in range(10000):
        
        tbsky.receiveData(dqueue[i],locatlist[i])
        tbsky.updateSkyline()
    
    totaltime = time.time() - start_time
    print("--- %s seconds ---" % (totaltime))
    # path = 'tbsky.txt'
    # f = open(path,'a+')
    # f.write('========== poccess = {a} ==========\n' . format(a=totaltime))
        
    #     if i > 80: #for plot part of result
    #         ll= len(tbsky.skyline)
    #         tbsky.showSkyline(ll,i)
    
        # print("---------tbsky.getWindow()",i,"---------")
        # for w in tbsky.getWindow():
        #     print(w)
        # print("---------tbsky.skyline()",i,"---------")
        # print(len(tbsky.getSkyline()))
        # for s1 in tbsky.getSkyline():
        #     print(s1)
        # print("---------tbsky.skyline2()",i,"---------")
        # print(len(tbsky.getSkyline2()))
        # for s2 in tbsky.getSkyline2():
        #     print(s2)
        
        
        # if i ==10:
        #     break
        # else:
        #     continue
    # print("---------tbsky.skyline2()---------")
    # for s2 in tbsky.getSkyline2():
    #     print(s2)     
    # print("tbsky.getWindow()",tbsky.getWindow())
    # print("tbsky.getSkyline()",tbsky.getSkyline())
    #    # print("tbsky.getSkyline2()",tbsky.getSkyline2())
    
    # plt.tight_layout()
    # plt.show()