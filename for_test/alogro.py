import math
if __name__ == '__main__':
    
    n = int(input("input the number"))
    j = math.ceil(n/2)
    temp = int(1)
    while (temp<=(j)):
        if (temp*temp>n):
            temp=temp-1
            break
        elif(temp*temp==n):
            break
        else:
            temp+=1
    print("result is ",temp)