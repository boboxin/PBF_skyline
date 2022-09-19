import os, sys

sys.path.append(os.path.abspath(os.pardir))

import pickle

import time

from data.dataClass import Data, batchImport

from skyline.slideUPSky import slideUPSky

from skyline.PSky import PSky

from visualize import visualize

# PSky class use only in server side 

class servePSky(PSky):

    def __init__(self, dim, ps, radius, drange=[0,1000], wsize=10):

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

            Note that the window size should be sum(edge window)

        """

        PSky.__init__(self, dim, ps, radius, drange, wsize)

    def receive(self,data):

        """

        Update data received by server

        :param data: dict

            json format(dict) data include change of an edge node.

            Delete: outdated data

            SK1: new data in skyline set

            SK2: new data in skyline2 set

        """

        # print("data list is",data)

        # print("data[0] list is",data[0])

        if len(data[0]['Delete']) > 0:

            # print("get in delete")

            for d in data[0]['Delete']:

                if d in self.window:

                    self.window.remove(d)

                    self.outdated.append(d)

                    self.updateIndex(d, 'remove')

                    

        if len(data[0]['SK1']) > 0:

            # print("get in sk1")

            for d in data[0]['SK1']:

                if d not in self.window:

                    self.window.append(d)

                    self.skyline.append(d)

                    self.updateIndex(d, 'insert')

                elif d in self.skyline2:

                    self.skyline2.remove(d)

                    self.skyline.append(d)

                # ignore other condition

        if len(data[0]['SK2']) > 0:

            # print("get in sk2")

            for d in data[0]['SK2']:

                if d not in self.window:

                    self.window.append(d)

                    self.skyline2.append(d)

                    self.updateIndex(d, 'insert')

                elif d in self.skyline:

                    self.skyline.remove(d)

                    self.skyline2.append(d)

                # ignore other condition

        self.update()

    def update(self):

        """

        Update global skyline set

        """

        if len(self.outdated) > 0:

            # Remove outdated data in sk2

            for d in self.outdated:

                if d in self.skyline2:

                    self.skyline2.remove(d)

            # Remove outdated data in sk, add sk2 data to sk when needed

            for d in self.outdated:

                if d in self.skyline:

                    self.skyline.remove(d)

                    sstart = [ i for i in d.getLocationMax()]

                    send = [self.drange[1] for i in range(self.dim)]

                    search = [ p.object for p in (self.index.intersection(tuple(sstart+send),objects=True))]

                    for sd in search:

                        if sd in self.skyline2:

                            self.skyline2.remove(sd)

                            self.skyline.append(sd)

            # Clear outdated data

            self.outdated = []

        # prune objects in sk, move data dominated by other sk point to sk2

        for d in self.skyline.copy():

            if d in self.skyline:

                vurstart = [ self.drange[1] if i+2*self.radius+0.1 > self.drange[1] else i+2*self.radius+0.1 for i in d.getLocationMax()]

                vurend = [ self.drange[1] for i in range(self.dim)]

                vur = [ p.object for p in (self.index.intersection(tuple(vurstart+vurend),objects=True))]

                for p in vur:

                    if p in self.skyline:

                        self.skyline.remove(p)

                        self.skyline2.append(p)

        # prune objects in sk2

        for d in self.skyline2.copy():

            if d in self.skyline2:

                vurstart = [ self.drange[1] if i+2*self.radius+0.1 > self.drange[1] else i+2*self.radius+0.1 for i in d.getLocationMax()]

                vurend = [ self.drange[1] for i in range(self.dim)]

                vur = [ p.object for p in (self.index.intersection(tuple(vurstart+vurend),objects=True))]

                for p in vur:

                    if p in self.skyline2:

                       self.skyline2.remove(p)


if __name__ == "__main__":

    rank=(10,12,14,16)

    #path ='test_node_result.txt'

    #r = open(path,'a+')

    for num in rank:
        
        path ='test_node_100000result.txt'

        r = open(path,'a+')

        ### localedge

        edgenum = num

        etmax = []

        print("----- amount of nodes ", edgenum," ------")

        r.write('------ amount of nodes : {a} -------\n'.format(a=edgenum))

        for k in range(edgenum):           

            eid = str(k)

            usky = slideUPSky(2, 5, 5, [0,1000], wsize=300)

            dqueue = batchImport('100000_dim2_pos5_rad5_01000.csv', 5)



            idx = [i for i in range(100000) if i%edgenum == k]

            with open('pickle_edge'+eid+'.pickle', 'wb') as f:

                start_time = time.time()

                for i in idx:

                    oldsk = usky.getSkyline().copy()

                    oldsk2 = usky.getSkyline2().copy()

                    usky.receiveData(dqueue[i])

                    out = usky.getOutdated().copy()

                    usky.updateSkyline()

                    usk1 = list(set(usky.getSkyline())-set(oldsk))

                    usk2 = list(set(usky.getSkyline2())-set(oldsk2))

                    result = {'Delete':out,'SK1':usk1,'SK2':usk2}

                    pickle.dump(result, f)

                finish_time= time.time() - start_time

                etmax.append(finish_time)

                print("edge",k+1,"process --- %s seconds ---" % (finish_time))

                r.write('node number {a} get {b} data process {c} second\n'.format(a=k+1,b=len(idx),c=finish_time))

                

            usky.removeRtree()

            

        r.write('the slowest edge is :{a}\nedge max time is {b}\ntotal edge mean is {c} \n'

                    .format(a=(etmax.index(max(etmax))+1),b=max(etmax),c=(sum(etmax)/len(etmax))))

        

        ### template_picklefile

        edgedata =[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        for e in range(edgenum):

            idx = [i for i in range(100000) if i%edgenum == e]

        

            with open('pickle_edge'+str(e)+'.pickle', 'rb') as f:

                for d in idx:

                    edgedata[e].append(pickle.load(f))

            

        ###localserver

        

        skyServer = servePSky(2, 5, 5, drange=[0,1000], wsize=300)

        server_time = time.time()-time.time() # let time be 0

        

        for k in range(100000):

            # pop list node by node

            m =k % edgenum               

            start_time = time.time()

            skyServer.receive(edgedata[m])

            skyServer.update()

            t=time.time() - start_time # just calculate the recieve and update time

            edgedata[m].pop(0)

            server_time = server_time+t

        print("--- finish --- %s seconds ---" % (server_time))

        skyServer.removeRtree()

        ### write into the file

        r.write('server cost time {a} \n'

                    .format(a=server_time))

        r.write('server+max edge time {a}\n\n'.format(a=server_time+max(etmax)))
        
        print("Output write into ",path)


