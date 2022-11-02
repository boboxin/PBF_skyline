# Test different possible instance
# Data: 1000 records, 2D, radius = 5
# Data: instance from 2 to 10
# Sliding window = 300
import os, sys
sys.path.append(os.path.abspath(os.pardir))

import time

# from .. import PBF
from PBF import pbfsky, batchImport,gravity

def instance_time():
    print('=== Test how instance count affect running time ===')
    inst = [3, 4, 5, 6, 7, 8, 9, 10]
    for ins in inst:
        path = 'pdfex_inst_result-nosk2.txt'
        f = open(path,'a+')
        indata = batchImport('10000_dim2_pos'+str(ins)+'_rad5_01000.csv', ins)
        dqueue = indata[0] #turn inputlist to dqueue
        locatlist = indata[1] #location for

        print('========== instance count = '+ str(ins) + ' ==========')
        print('---------- Brute force ----------')
        tbsky = pbfsky(10000,2, ins, 5, [0,1000], wsize=300)
        
        start_time = time.time()
        for i in range(10000):
            tbsky.receiveData(dqueue[i],locatlist[i])
            tbsky.updateSkyline()
        itime1 = time.time()- start_time 
        print("--- %s seconds ---" % (itime1))
        f.write('========== Data instance = {a} ==========\n' . format(a=tbsky.ps))
        f.write('instance:{a} ; time:{b}\n'.format(a=tbsky.ps,b= itime1))


def instance_avgsk():
    print('=== Test how instance count affect candidate skyline ===')
    inst = [3, 4, 5, 6, 7, 8, 9, 10]
    for ins in inst:
        path = 'pdfex_inst_result-nosk2.txt'
        path2 = 'pdfex_inst_skresult.txt'
        f = open(path,'a+')
        f2 = open(path2,'a+')
        indata = batchImport('10000_dim2_pos'+str(ins)+'_rad5_01000.csv', ins)
        dqueue = indata[0] #turn inputlist to dqueue
        locatlist = indata[1] #location for

        
        print('========== instance count = '+ str(ins) + ' ==========')
        print('---------- Brute force ----------')
        tbsky = pbfsky(10000,2, ins, 5, [0,1000], wsize=300)
        f2.write('========== Data instance = {a} ==========\n' . format(a=tbsky.ps))
        avgsk1, avgsk2 = 0, 0
        for i in range(10000):
            tbsky.receiveData(dqueue[i],locatlist[i])
            tbsky.updateSkyline()
            avgsk1 += len(tbsky.getSkyline())
            f2.write('\n========== time slot = {a} ==========\n' . format(a=i))
            f2.write('skyilne size : {a}\n'  . format(a=len(tbsky.getSkyline())))
            for s1 in tbsky.getSkyline():
                f2.write('{a}\n'  . format(a=s1))
            # avgsk2 += len(tbsky.getSkyline2())
        # tbsky.removeRtree()
        avgsk1 = avgsk1/10000
        # avgsk1, avgsk2 = avgsk1/10000, avgsk2/10000
        print('Avg. sky1: '+ str(avgsk1))
        # print('Avg. sky2: '+ str(avgsk2))
        f.write('========== Data instance = {a} ==========\n' . format(a=tbsky.ps))
        f.write('Avg. sky1:{a} \n'.format(a=avgsk1))
        

if __name__ == '__main__':
    print("1: Test time\n2: Test average skyline size \n3: Run all test")
    switch = int(input('Choose your test: '))
    if switch == 1: # test time
        instance_time()
    elif switch == 2: # test avg sky
        instance_avgsk()
    elif switch == 3:
        instance_time()
        instance_avgsk()
    else:
        print('error')