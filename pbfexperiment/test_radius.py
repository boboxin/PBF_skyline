# Test different radius
# Data: 1000 records, 2D, instance = 5
# Data: radius from 3 to 10
# Sliding window = 300

import os, sys
sys.path.append(os.path.abspath(os.pardir))

import time

# from data.dataClass import batchImport
# from skyline.slideBPSky import slideBPSky
# from skyline.slideUPSky import slideUPSky

# from .. import PBF
from PBF import pbfsky, batchImport,gravity

def radius_time():
    print('=== Test how data radius affect running time ===')
    radius = [4, 6, 8, 10, 12, 14, 16, 18, 20]
    for r in radius:
        path = 'pdfex_radius_result.txt'
        f = open(path,'a+')
        dqueue = batchImport('10000_dim2_pos5_rad'+str(r)+'_01000.csv', 5)
        inputlist = dqueue[0]
        inputarray = dqueue[1]#location for

        print('========== radius = '+ str(r) + ' ==========\n')
        print('---------- Brute force ----------')
        tbsky = pbfsky(2, 5, r, [0,1000], wsize=300)
        glist=gravity(inputarray,tbsky.ps,tbsky.dim)# turn uncertain data into certain data
        
        start_time = time.time()
        for i in range(10000):
            tbsky.receiveData(glist[i])
            tbsky.updateSkyline()
        rtime1= time.time() - start_time
        print("--- %s seconds ---" % (rtime1))
        f.write('========== Data radius = {a} ==========\n' . format(a=tbsky.radius))
        f.write('radius:{a} ; time:{b}\n'.format(a=tbsky.radius,b= rtime1))
        
def radius_avgsk():
    print('=== Test how data radius affect candidate skyline ===')
    radius = [4, 6, 8, 10, 12, 14, 16, 18, 20]
    for r in radius:
        path = 'pdfex_radius_result.txt'
        f = open(path,'a+')
        dqueue = batchImport('10000_dim2_pos5_rad'+str(r)+'_01000.csv', 5)
        inputlist = dqueue[0]
        inputarray = dqueue[1]#location for
        
        print('========== radius = '+ str(r) + ' ==========')
        print('---------- Brute force ----------')
        tbsky = pbfsky(2, 5, r, [0,1000], wsize=300)
        glist=gravity(inputarray,tbsky.ps,tbsky.dim)# turn uncertain data into certain data
        
        avgsk1, avgsk2 = 0, 0
        for i in range(10000):
            tbsky.receiveData(glist[i])
            tbsky.updateSkyline()
            avgsk1 += len(tbsky.getSkyline())
            avgsk2 += len(tbsky.getSkyline2())
        # tbsky.removeRtree()
        avgsk1, avgsk2 = avgsk1/10000, avgsk2/10000
        print('Avg. sky1: '+ str(avgsk1))
        print('Avg. sky2: '+ str(avgsk2))
        f.write('========== Data radius = {a} ==========\n' . format(a=tbsky.radius))
        f.write('Avg. sky1:{a} ; Avg. sky2:{b}\n'.format(a=avgsk1,b= avgsk2))
        

if __name__ == '__main__':
    print("1: Test time\n2: Test average skyline size \n3: Run all test")
    switch = int(input('Choose your test: '))
    if switch == 1: # test time
        radius_time()
    elif switch == 2: # test avg sky
        radius_avgsk()
    elif switch == 3:
        radius_time()
        radius_avgsk()
    else:
        print('error')