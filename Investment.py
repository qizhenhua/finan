#!/usr/bin/python3
#This program is written by Qi ZhenHua!
#Description:
#Usage:
#code is below.

class Investment(object):
    import datetime
    def __init__(self,fundcode="001593"):
        self.Datelist=[]
        self.NAVlist=[]
        self.Investlist=[]
        self.tableNAV={}
        self.readfund(fundcode)

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
        self.tableNAV=dict(zip(self.Datelist,self.NAVlist))
        self.clearaccount()

    def clearaccount(self):
        self.Investlist = []
        for i in range(len(self.NAVlist)):
            self.Investlist.append(0.0)

    def indexdate(self,date):
        for i in range(len(self.Datelist)):
            if date<=self.Datelist[i]:
                return i
        return i

    def dateprevious(self,datetrade,previousdays):
        """return a date list of previouse days of trade date, not include trade day"""
        i = self.indexdate(datetrade)
        j = i - previousdays
        if j < 0:
            j = 0
        return self.Datelist[j:i]

    def datenext(self,datetrade,nextdays):
        i = self.indexdate(datetrade)
        j = i + nextdays
        if j > len(self.Datelist):
            j = self.Datelist[-1]
        return self.Datelist[i:j]

    def dataperiod(self, datestart, dateend):
        """retrun a dict of data of date/NAV/investmoney"""
        i=self.indexdate(datestart)
        j=self.indexdate(dateend) + 1
        result = dict(zip(["date",             "NAV",             "investmoney"       ], \
                          [self.Datelist[i:j], self.NAVlist[i:j], self.Investlist[i:j]]))
        return result

    def NAVaverage(self,datestart,dateend):
        myNAVlist=self.dataperiod(datestart,dateend)["NAV"]
        sumNAV=0.0
        for price in myNAVlist:
            sumNAV += price
        return sumNAV/len(myNAVlist)

    def rategrowth(self):
        """calculate growth rate for each day, return a whole list"""
        result=[0]
        for i in range(1,len(self.NAVlist)):
            a=(self.NAVlist[i]-self.NAVlist[i-1])/self.NAVlist[i-1]
            result.append(a)
        return result

    def capitalinvested(self):
        """calculate invested money of all"""
        result=0.0
        for i in self.Investlist:
            result += i
        return result

    def sharesaved(self):
        result=0.0
        for i in zip(self.Investlist,self.NAVlist):
            result += i[0]/i[1]
        return result

    def priceaverage(self):
        return self.capitalinvested()/self.sharesaved()

    def buy(self,date,money):
        i=self.indexdate(date)
        self.Investlist[i] = self.Investlist[i] + money

    def sell(self,date):
        price=self.tableNAV[date]
        capital=self.capitalinvested()
        share=self.sharesaved()
        money=share * price
        rate=(money-capital)/capital
        result=dict(zip(["capital","money","rate","bonus"],\
                        [capital,money,rate,money-capital]))
        return result

    def printinvestment(self,datestart,dateend=""):
        if dateend == "":
            dateend = self.Datelist[-1]
        a=self.dataperiod(datestart,dateend)
        dates=a["date"]
        NAVs=a["NAV"]
        money=a["investmoney"]
        datas=list(zip(dates,NAVs,money))
        for i in datas:
            print(i)

    def investregular(self,datestart,dateend,moneyregular):
        """The simplest investing mode, set start date / end date / money for each day, it will set money to the list
        """
        istart=self.indexdate(datestart)
        iend=self.indexdate(dateend)
        i=0
        datetrade=datestart
        while datetrade < dateend:
            self.buy(datetrade,moneyregular)
            datetrade=self.Datelist[istart+i]
            i += 1

    def investstrategy01(self,datestart,moneypiece,ratetarget,daysmin,):
        """Set a bonus rate target, if reach the bonus rate, sell the share"""
        days = 0
        dateend=self.Datelist[-1]
        mydatelist=self.dataperiod(datestart,dateend)["date"]
        for datetrade in mydatelist:
            self.buy(datetrade,moneypiece)
            days += 1
            if days> daysmin and self.sell(datetrade)["rate"] >= ratetarget:
                break
        return datetrade

    def investstrategy02(self,datestart,moneypiece,ratetarget,daysmin,ratelowerlimit=-100,factor=0):
        """Set a bonus rate garget, in investing period, buy more share (factor * moneypiece) when
           price fall over lower limit
        """
        days = 0
        dateend=self.Datelist[-1]
        mydatelist=self.dataperiod(datestart,dateend)["date"]
        dateprevious=datestart
        for datetrade in mydatelist:
            self.buy(datetrade,moneypiece)
            days += 1
            if days> daysmin and self.sell(datetrade)["rate"] >= ratetarget:
                break
            #below codes are different from previous strategy
            temp=self.dateprevious(datetrade,3) # trade day previous 3 days
            temp=self.NAVaverage(temp[0],temp[-1])  #get it average price
            temp=(self.tableNAV[datetrade] - temp)/ temp  #calculate down rate
            if  temp < ratelowerlimit: # and self.tableNAV[datetrade] < 1.45:
                self.buy(datetrade,moneypiece*factor)
            dateprevious=datetrade
        return datetrade

    def investstrategy03(self,datestart,moneypiece=10,ratetarget=0.20,daysmin=10,factor=10):
        """Set a bonus rate garget, in investing period, buy more share (factor * moneypiece) when
           price fall over average price.
        """
        days = 0
        dateend=self.Datelist[-1]
        mydatelist=self.dataperiod(datestart,dateend)["date"]
        dateprevious=datestart
        for datetrade in mydatelist:
            self.buy(datetrade,moneypiece)
            days += 1
            if days> daysmin and self.sell(datetrade)["rate"] >= ratetarget:
                break
            #below codes are different from previous strategy
            
            pricecurrent=self.tableNAV[datetrade]  #calculate down rate
            if  pricecurrent < 0.98*self.priceaverage(): # it worth buy
                self.buy(datetrade,moneypiece*factor)
        return datetrade

    def testing01(self):
        pass

fundlist=["001016","001593","002385","002903","002987","003766","004342","004343","004348","004744","004870",
          "005633","005658","005918","005919","006087","006131","006912","070039","160724","260108","501037",
          "519019"]

for fundname in fundlist:
    a=Investment(fundname)
    buydate="2018-01-04"
    selldate="2019-04-01"
    print("investing from %s to %s-----------------------------------"%(buydate,fundname))
    print("-------------regular investing:---------")
    a.investregular(buydate,selldate,10)
    print(a.sell(selldate))
    print(selldate)
    a.clearaccount()
    print("-------------Strategy 1:---------")
    b=a.investstrategy01(buydate,10,0.10,10)
    print(a.sell(b))
    print(b)
    a.clearaccount()

##    print("-------------Strategy 2:---------")
##
##    b=a.investstrategy02(buydate,10,0.12,10,-0.04,50)
##    print(a.sell(b))
##    print(b)
##    a.clearaccount()
##
##    b=a.investstrategy02(b,10,0.12,10,-0.04,50)
##    print(a.sell(b))
##    print(b)
##    a.clearaccount()

    print("-------------Strategy 3:---------")
    temp="2018-01-24"
    b=a.investstrategy03(temp,10,0.20,10,10)
    print(a.sell(b))
    print(b)
    #a.printinvestment(temp,b)
    a.clearaccount()


#if you want to make it as a module, remove below code's #
#def main():
#
#if __name__=="__main__":
#    main()
