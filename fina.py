#!/usr/bin/python3
#This program is written by Qi ZhenHua!
#Description:
#Usage:
#code is below.
NAVlist=[]
myfile=open("./data/"+input("Input data file:")+".csv","r")
a=myfile.readlines()
myfile.close()
datelist=[]
for i in a:
    b=i.split(',')
    c=b[2].split('\n')[0]
    if c!='NAV':
        NAVlist.append(float(c))
        datelist.append(b[1])

def invest(StartN,initA,mylist,limit):
    share,money,rate,base,i=0.0,0.0,0.0,0.0,0
    while rate<=limit and StartN+i<len(mylist):
        share=initA/mylist[StartN+i]+share
        money=share*mylist[StartN+i]
        base=initA*(i+1)
        rate=money/base-1
        i+=1
    flag=""
    if StartN+i==len(mylist):
        print("Bad->Start: %s, price %f, you need to wait"% (datelist[StartN],NAVlist[StartN]))
        flag="bad"
    else:
        if i>20 and i<64: # 1 to 3 months
            flag="good"
            print("Good invest-->",end=" ")
        else:
            flag="not good"
        print("Start: %s, price %f, End: %s, price %f, bonus rate: %f,invest money %f, back money %f at %dth days."
              %(datelist[StartN],NAVlist[StartN],datelist[StartN+i],NAVlist[StartN+i],rate,base,money,i))
    return flag

countbad,countgood=0,0
for j in range(0, len(NAVlist)):
    myflag=invest(j,10,NAVlist,0.04)
    if myflag=="good":
        countgood+=1
    if myflag=="bad":
        countbad+=1
print("Result: you have invest %d times, good %d(%f%%), bad %d(%f%%), other %d(%f%%)"
          %(j,countgood,(countgood/j*100),countbad,(countbad/j*100),j-countgood-countbad,((j-countgood-countbad)/j*100)))



#if you want to make it as a module, remove below code's #
#def main():
#
#if __name__=="__main__":
#    main()

