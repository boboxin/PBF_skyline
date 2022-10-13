# Test different sliding window size
# Data: 1000 records, 2D, possible instance = 5, radius = 5
# Sliding window from 100 to 1000, increase by 100
import os, sys
sys.path.append(os.path.abspath(os.pardir))

import time

# from data.dataClass import batchImport
# from skyline.slideBPSky import slideBPSky
# from skyline.slideUPSky import slideUPSky

# from .. import PBF
from PBF import pbfsky, batchImport,gravity

def wsize_time():
    print("=== Test how window size affect running time ===")
    wsize = [100,200,300,400,500,600,700,800,900,1000]
    indata = batchImport('10000_dim2_pos5_rad5_01000.csv', 5)
    dqueue = indata[0] #turn inputlist to dqueue
    locatlist = indata[1] #location for
    for w in wsize:
        path = 'pdfex_win_result-nosk2.txt'
        f = open(path,'a+')
        print('========== window size = '+ str(w) + ' ==========')
        print('---------- Brute force ----------')
        tbsky = pbfsky(10000,2, 5, 5, [0,1000], wsize=w)
        start_time = time.time()
        for i in range(10000):
            tbsky.receiveData(dqueue[i],locatlist[i])
            tbsky.updateSkyline()
        wtime1 = time.time() - start_time
        print("--- %s seconds ---" % (wtime1))
        f.write('========== Data window_size = {a} ==========\n' . format(a=tbsky.wsize))
        f.write('win size:{a} ; time:{b}\n'.format(a=tbsky.wsize,b= wtime1))
        

def wsize_avgsk():
    print("=== Test how window size affect candidate skyline ===")
    wsize = [100,200,300,400,500,600,700,800,900,1000]
    indata = batchImport('10000_dim2_pos5_rad5_01000.csv', 5)
    dqueue = indata[0] #turn inputlist to dqueue
    locatlist = indata[1] #location for
    for w in wsize:
        print('========== window size = '+ str(w) + ' ==========')
        print('---------- Brute force ----------')
        tbsky = pbfsky(10000,2, 5, 5, [0,1000], wsize=w)
        avgsk1, avgsk2 = 0, 0
        path = 'pdfex_win_result-nosk2.txt'
        f = open(path,'a+')
        for i in range(10000):
            tbsky.receiveData(dqueue[i],locatlist[i])
            tbsky.updateSkyline()
            avgsk1 += len(tbsky.getSkyline())
            # avgsk2 += len(tbsky.getSkyline2())
        avgsk1 = avgsk1/10000
        # avgsk1, avgsk2 = avgsk1/10000, avgsk2/10000
        print('Avg. sky1: '+ str(avgsk1))
        # print('Avg. sky2: '+ str(avgsk2))
        f.write('========== Data win size = {a} ==========\n' . format(a=tbsky.wsize))
        f.write('Avg. sky1:{a} \n'.format(a=avgsk1))
        
if __name__ == '__main__':
    print("1: Test time\n2: Test average skyline size \n3: Run all test")
    switch = int(input('Choose your test: '))
    if switch == 1: # test time
        wsize_time()
    elif switch == 2: # test avg sky
        wsize_avgsk()
    elif switch == 3:
        wsize_time()
        wsize_avgsk()
    else:
        print('error')
