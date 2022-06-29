# Sliding window update PSky
import os, sys
from pickle import EMPTY_LIST
sys.path.append(os.path.abspath(os.pardir))
import os
import csv
import numpy as np
import random
from data.dataClass import Data, batchImport
here = os.path.dirname(os.path.abspath(__file__))
import time

skylinelist = []

#test data
entry1 = [11,1,1] # [sequenceID, objectpoint, itemtag 1:EX ; 0:SK]
entry2 = [11,2,0]
entry3 = [11,3,0]
entry4 = [11,6,0]
eventlist = [entry1,entry2,entry3,entry4]


currenttime = time.time()
def procExpiration():
    if len(eventlist) == 0:
        print('list is empty')
    else:
        if eventlist[0][2] == 1:  #itemtag in entry1
            eventlist.pop(0)
        else:
            eventlist[0][2] = 1   #還要處理timestamp&influence time&window side的問題
            skylinelist.append(eventlist[0])
            eventlist.pop(0)
            eventlist.append(skylinelist[-1])
        print("sl:", skylinelist)
        print("el:", eventlist)
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
    with open(here+'/'+csvfile, 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        for row in csv_reader:
            data = Data(row[0], ps)
            for p in range(ps):
                # Some awful string manipulation to parse numbers
                data.insertLocation(float(row[2*p+1]), [int(float(i)) for i in row[2*p+2].strip(' []').split(',')])
            result.append(data)
    return result
# def receiveData(self, d):
#         """
#         Receive one new data.

#         :param d: Data
#             The received data
#         """
#         if len(self.window) >= self.wsize:
#             self.updateIndex(self.window[0], 'remove')
#             del self.window[0]
#         self.window.append(d)
#         self.updateIndex(d,'insert')      
if __name__ == '__main__':
    # while len(eventlist)!=0 :
    vol = batchImport('test_30_dim2_pos3_rad2_0100.csv',3)
    
    for i in range(30):
        print(vol[i])
    # for i in range(len(eventlist)):
    #     procExpiration()
    
