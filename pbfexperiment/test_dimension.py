# Test different data dimension
# Data: 1000 records, possible instance = 5, radius = 5
# Data: dimension from 2 to 10
# Sliding window = 300
import os, sys
sys.path.append(os.path.abspath(os.pardir))

import time

from .. import PBF
from PBF import pbfsky, batchImport


def dim_time():
    print("=== Test how dimension of data affect running time ===")
    dim = [2, 3, 4, 5, 6, 7, 8, 9, 10]

    for d in dim:
        path = 'pdfex_dim_result.txt'
        f = open(path,'a+')
        dqueue = batchImport('10000_dim'+str(d)+'_pos5_rad5_01000.csv', 5)
        print('========== Data dimension = '+ str(d) + ' ==========')
        print('---------- Brute force ----------')
        tbsky = pbfsky(d, 5, 5, [0,1000], wsize=300)
        start_time = time.time()

        for i in range(10000):
            tbsky.receiveData(dqueue[i])
            tbsky.updateSkyline()
        dtime1 = time.time() - start_time
        print("--- %s seconds ---" % (dtime1))
        f.write('========== Data dimension = {a} ==========' . format(a=tbsky.dim))
        f.write('dimension:{a} ; time:{b} '.format(a=tbsky.dim,b= dtime1))
        
def dim_avgsk():
    print("=== Test how dimension of data affect candidate size ===")
    dim = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    for d in dim:
        path = 'pdfex_dim_result.txt'
        f = open(path,'a+')
        dqueue = batchImport('10000_dim'+str(d)+'_pos5_rad5_01000.csv', 5)
        print('========== Data dimension = '+ str(d) + ' ==========')
        print('---------- Brute force ----------')
        tbsky = pbfsky(d, 5, 5, [0,1000], wsize=300)
        avgsk1, avgsk2 = 0, 0
        for i in range(10000):
            tbsky.receiveData(dqueue[i])
            tbsky.updateSkyline()
            avgsk1 += len(tbsky.getSkyline())
            avgsk2 += len(tbsky.getSkyline2())
        # tbsky.removeRtree()
        avgsk1, avgsk2 = avgsk1/10000, avgsk2/10000
        print('Avg. sky1: '+ str(avgsk1))
        print('Avg. sky2: '+ str(avgsk2))
        f.write('========== Data dimension = {a} ==========' . format(a=tbsky.dim))
        f.write('Avg. sky1:{a} ; Avg. sky2:{b} '.format(a=avgsk1,b= avgsk2))
        
if __name__ == '__main__':
    print("1: Test time\n2: Test average skyline size \n3: Run all test")
    switch = int(input('Choose your test: '))
    if switch == 1: # test time
        dim_time()
    elif switch == 2: # test avg sky
        dim_avgsk()
    elif switch == 3:
        dim_time()
        dim_avgsk()
    else:
        print('error')
