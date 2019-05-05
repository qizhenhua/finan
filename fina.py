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

def calculate(startN,endN,initA,mylist,limit):
    share=0.0
    money=0.0
    rate=0.0
    targetrates=[]
    dateseq=[]
    base=0.0
    for i in range(startN,endN):
        share=initA/mylist[i]+share
        money=share*mylist[i]
        base=initA*(i-startN+1)
        rate=money/base-1
        if rate>=limit:
            targetrates.append(rate)
            dateseq.append(i-startN)
        #print("%d,%f3,%f,%f3"%(i,rate,base,money))
    result=list(zip(dateseq,targetrates))
    #print("The last result: %f,%f,%f"%(rate,base,money))
    print("You have %d chances to save money!"% len(result),end="-->")
    if dateseq==[]:
        print("You will lost money! %f of %f"%( (money-base),base))
    else:
        print("The first/last chance is in the %d & %d days!"% (dateseq[0],dateseq[len(dateseq)-1]))
    return result

#start=int(input("Input start N(date): "))
#end=int(input("Input end N(date): "))
#a=float(input("Input money every day: "))
#calculate(start,end,a,NAVlist)
#print("You should have base %f"%(a*(end-start)))
for i in range(0,len(NAVlist)-100):
    print("Start:",datelist[i],end="--")
    calculate(i,i+99,20,NAVlist,0.025)


#if you want to make it as a module, remove below code's #
#def main():
#
#if __name__=="__main__":
#    main()

