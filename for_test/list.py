

if __name__ == "__main__":
    datalist = [{'Delete': [555], 'SK1': ['asdf'], 'SK2': [55555]}, 
                {'Delete': [], 'SK1': [5], 'SK2': []}, 
                {'Delete': [], 'SK1': [], 'SK2': [5]}]
    # for i in range (3):
    #     for k in range (2):
            
    #         datalist[i].append(i+k)
    
    #         print("i=",i,"k=",k,";",datalist[i][k])
            
    # print(datalist[0][0])
    # datalist2=datalist[0]
    # print(datalist2)
    # print(datalist2[0])
    if len(datalist[0]['Delete']) > 0:
        print("there is a Delete")
        print(datalist[0])
    elif len(datalist[0]['SK1']) > 0:
        print("there is a SK1")
        print(datalist[0])
        datalist.pop()
    elif len(datalist[0]['SK2']) > 0:
        print("there is a SK2")
        print(datalist[0])
        datalist.pop()
    else:
        print("bye")