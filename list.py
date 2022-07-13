

if __name__ == "__main__":
    datalist = [[],[],[]]
    for i in range (3):
        for k in range (2):
            
            datalist[i].append(i+k)
    
            print("i=",i,"k=",k,";",datalist[i][k])
            
    print(datalist[0][0])
    datalist2=datalist[0]
    print(datalist2)
    print(datalist2[0])