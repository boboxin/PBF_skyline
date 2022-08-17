import os
import csv
import numpy as np



here = os.path.dirname(os.path.abspath(__file__))
class PSky():
    def __init__(self, dim, ps, radius, drange, wsize):
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
        self.dim = dim # data dimension
        self.ps = ps # possible instance count
        self.radius = radius # radius of a data
        self.drange = drange # data range
        self.wsize = wsize # sliding window size
        self.window = [] # sliding window
        self.skyline = [] # 1st set skyline candidate
        self.skyline2 = [] # 2nd set skyline candidate
        self.outdated = [] # temporary storage for outdated data
        # p = index.Property()
        # p.dimension = dim
        # p.dat_extension = 'data'
        # p.idx_extension = 'index'
        # self.index = index.Index(str(dim)+'d_index',properties=p) # r-tree index
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
    with open(here+'/data/'+csvfile, 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        for row in csv_reader:
            data = Data(row[0], ps)
            for p in range(ps):
                # Some awful string manipulation to parse numbers
                data.insertLocation(float(row[2*p+1]), [int(float(i)) for i in row[2*p+2].strip(' []').split(',')])
                locat = data.getLocation(p)
                # print(local)
                locatlist.append(locat)
                larray = np.array(locatlist)# use array data type to return
                # print(larray[p],type(larray),larray.shape)
                
                
            result.append(data) #all is in a list
    return result,larray

if __name__ == '__main__':
    
    test = pbfsky(2, 5, 5, [0,1000], wsize=20)
    indata = batchImport('100_dim2_pos5_rad5_01000.csv',test.ps)
    inputlist = indata[0]
    inputarray = indata[1]#location for
    glist=gravity(inputarray,test.ps,test.dim)# turn uncertain data into certain data


    for i in range(100):
        
        test.receiveData(glist[i])
        test.updateSkyline()
        
        print("test.getWindow()",test.getWindow())
        print("test.getSkyline()",test.getSkyline())
        print("test.getSkyline2()",test.getSkyline2())        