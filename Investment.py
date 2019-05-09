#!/usr/bin/python3
#This program is written by Qi ZhenHua!
#Description:
#Usage:
#code is below.

# #fundlist=["001016","001593","002385","002903","002987","003766","004342","004343","004348","004744","004870",
# #          "005633","005658","005918","005919","006087","006131","006912","070039","160724","260108","501037",
# #          "519019"]

class Investment(object):
    import datetime
    def __init__(self,fundcode):
        self.Datelist=[]
        self.NAVlist=[]
        self.Investlist=[]
        self.readfund(fundcode)
        self.clearaccount()

    def readfund(self,filename):
        myfile = open("./data/" + filename + ".csv", "r")
        a=myfile.readlines()
        myfile.close()
        for i in a:
            b=i.split(',')
            c=b[2].split('\n')[0]
            if c!='NAV':
                self.NAVlist.append(float(c))
                self.Datelist.append(b[1])

    def clearaccount(self):
        self.Investlist = []
        for i in range(len(self.NAVlist)):
            self.Investlist.append(0.0)

    def indexdate(self,date):
        for i in range(len(self.Datelist)):
            if date<=self.Datelist[i]:
                return i

    def buy(self,date,money):
        i=self.indexdate(date)
        self.Investlist[i] = self.Investlist[i] + money

    def sell(self,date):
        indexend=self.indexdate(date)
        price=self.NAVlist[indexend]
        capital,share=0.0,0.0
        for i in range(len(self.Datelist)):
            if self.Investlist[i]>0:
                capital += self.Investlist[i]
                share += self.Investlist[i]/self.NAVlist[i]
        money=share * price
        rate=((money-capital)/capital)*100
        return capital,money,rate

    def investregular(self,datestart,dateend,moneyregular):
        istart=self.indexdate(datestart)
        iend=self.indexdate(dateend)
        i=0
        datetrade=datestart
        while datetrade < dateend:
            self.buy(datetrade,moneyregular)
            datetrade=self.Datelist[istart+i]
            i += 1

    def investregulartarget(self,datestart,moneyregula,ratetarget,daysmin):
        istart=self.indexdate(datestart)
        i=0
        datetrade=datestart
        while datetrade < self.Datelist[-1]:
            self.buy(datetrade,moneyregula)
            datetrade=self.Datelist[istart+i]
            i += 1
            if i > daysmin and self.sell(datetrade)[2] >= ratetarget:
                break
        return datetrade

a=Investment("001593")
buydate="2018-01-04"
selldate="2019-04-01"

a.investregular(buydate,selldate,10)
print(a.sell(selldate))
a.clearaccount()

b=a.investregulartarget(buydate,10,16,10)
print(a.sell(b))
print(b)



#if you want to make it as a module, remove below code's #
#def main():
#
#if __name__=="__main__":
#    main()

