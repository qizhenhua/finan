#!/usr/bin/python3
#This program is written by Qi ZhenHua!
#Description:
#Usage:
#code is below.

class Marketfund(object):
    import datetime
    def __init__(self,fundcode="000961"):
        self.fundcode=fundcode
        self.Datelist=[]
        self.NAVlist=[]
        self.Investlist=[]
        self.Sharelist=[]
        self.tableNAV={}
        self.accountbank=10000.0
 
    def readfund(self,filename=""):
        if filename=="":
            filename=self.fundcode
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
        self.clearaccountfund()

    def splitdata(self,datestart,dateend=""):
        a=self.dataperiod(datestart,dateend)
        self.Datelist=a["date"]
        self.NAVlist=a["NAV"]
        self.Investlist=a["investmoney"]
        self.Sharelist=a["share"]
              

    def clearaccountfund(self):
        self.Investlist = []
        self.Pricestock = []
        for i in range(len(self.NAVlist)):
            self.Investlist.append(0.0)
            self.Sharelist.append(0.0)
        

    def indexdate(self,date):
        for i in range(len(self.Datelist)):
            if date<=self.Datelist[i]:
                return i
        return i

    def dateprevious(self,datetrade,previousdays=1):
        """return a date list of previouse days of trade date, not include trade day"""
        i = self.indexdate(datetrade)
        if i == 0:
            return [(self.Datelist[0])]
        j = i - previousdays
        if j < 0:
            j = 0
        return self.Datelist[j:i]

    def datenext(self,datetrade,nextdays):
        i = self.indexdate(datetrade)
        if i == self.Datelist[-1]:
            return list(self.Datelist[-1])
        i += 1
        j = i + nextdays
        if j > len(self.Datelist):
            j = self.Datelist[-1]+1
        return self.Datelist[i:j]

    def dataperiod(self, datestart, dateend=""):
        """retrun a dict of data of date/NAV/investmoney"""
        if dateend == "":
            dateend=self.Datelist[-1]
        i=self.indexdate(datestart)
        j=self.indexdate(dateend) + 1
        result = dict(zip(["date",             "NAV",             "investmoney",        "share"     ], \
                          [self.Datelist[i:j], self.NAVlist[i:j], self.Investlist[i:j], self.Sharelist[i:j]]))
        return result

    def NAVaverage(self,datestart,dateend):
        myNAVlist=self.dataperiod(datestart,dateend)["NAV"]
        sumNAV=0.0
        for price in myNAVlist:
            sumNAV += price
        return sumNAV/len(myNAVlist)

    def getrategrowth(self):
        """calculate growth rate for each day, return a whole list"""
        result=[0]
        for i in range(1,len(self.NAVlist)):
            a=(self.NAVlist[i]-self.NAVlist[i-1])/self.NAVlist[i-1]
            result.append(a)
        return result

    def moneyinvested(self):
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

    def getstocklist(self):
        sharecumulationlist=[]
        moneycumulationlist=[]
        pricestocklist=[]
        for datecurrent in self.Datelist:
            money,share=0.0,0.0
            period=self.dataperiod(self.Datelist[0],datecurrent)
            for investeach in period["investmoney"]:
                money += investeach
            for shareeach in period["share"]:
                share += shareeach
            if share <= 0.0:
                price=0
            else:
                price=money/share
            sharecumulationlist.append(share)
            moneycumulationlist.append(money)
            pricestocklist.append(price)
        result= dict(zip(self.Datelist,list(zip(pricestocklist,moneycumulationlist,sharecumulationlist))))
        return result

    def pricestock(self):            
        return self.moneyinvested()/self.sharesaved()

    def howmuchmoney2makestockpricedown(self,rate,pricetrade):
        """
        "I cann't control market price, but I can change my stock share price"---Qi Zhenhua 
        This function caluculate that how much money to change the stockprice (down or up)
        with rate, use pricetrade. base below setp:
        -----First, we have those equal functions
        shareadded=money/pricetrade     #1
        sharetotal=shareadded+self.sharesaved() #2
        moneytotal=money+self.moneyinvested() #3
        pricefinal=moneytotal/sharetotal #4
        rate=(pricefinal-self.pricestock())/self.pricestock() #5

        -----Now we change #5:
        pricefinal=self.pricestock()*(1+rate)  # 6
        -----Combine #3 and #4, we get:
        pricefinal=(money+self.moneyinvested())/sharetotal #7
        -----Continue change #7:
        money = pricefinal*sharetotal-self.moneyinvested() #7'
        -----Input #2 to #7':
        money = pricefinal*(shareadded+self.sharesaved())-self.moneyinvested()  #8
        -----Input #1 to #8:
        money = pricefinal*(money/pricetrade+self.sharesaved())-self.moneyinvested()
              = money*pricefinal/pricetrade+pricefinal*self.sharesaved()-self.moneyinvested()
        (1-pricefinal/pricetrade)*money = pricefinal*self.sharesaved()-self.moneyinvested()
        money=(pricefinal*self.sharesaved()-self.moneyinvested())/(1-pricefinal/pricetrade) #9

        -----Use #9 and #6, to make codes run    
        
        """
        ratelimit=(pricetrade-self.pricestock())/self.pricestock()  # the rate cann't out of range.
        money = 0
        if rate > -abs(ratelimit) and rate < abs(ratelimit):
            pricefinal=self.pricestock()*(1+rate)
            money=(pricefinal*self.sharesaved()-self.moneyinvested())/(1-pricefinal/pricetrade)
        else:
            print("rate must between +/- %f !"%abs(ratelimit))
        return money

    def howmuchmoney(self,datetrade):
        pricetrade=self.tableNAV[datetrade]  #calculate down rate
        if datetrade==self.Datelist[0]:
            lastday=datetrade
        else:
            lastday=self.dateprevious(datetrade,1)[0]
        pricelastday=self.tableNAV[lastday]
        pricestock=self.pricestock()
        if  pricetrade < pricestock and pricetrade < pricelastday: # it worth buy when trade price > stock price
            ratelimit=pricetrade/pricestock-1
            if ratelimit < -0.08:   # it avoid money uneffect
                rate=-0.05   # the money make the stockprice down raterange/3
                money=self.howmuchmoney2makestockpricedown(rate,pricetrade)
                
##                if money > 2000: # the money limit
##                    money =2000
            else:
                money=0
        else:
            money=0  # if trade price > stock price, you should sell it, not spend more money
        return money

    def checkaccountbank(self,datetrade,salarymonth=1000):
        datelast=self.dateprevious(datetrade,1)[0]
        lastmonth=datelast.split("-")[1]
        trademonth=datetrade.split("-")[1]
        if trademonth > lastmonth:
            self.accountbank += salarymonth
    
    def buy(self,date,money):
        if money > self.accountbank:
            money = self.accountbank
            self.accountbank=0.0
        else:
            self.accountbank -= money
        
        i=self.indexdate(date)
        self.Investlist[i] = self.Investlist[i] + money
        self.Sharelist[i] = self.Sharelist[i] + money/self.tableNAV[date]
        
    def sell(self,date):
        price=self.tableNAV[date]
        capital=self.moneyinvested()
        share=self.sharesaved()
        money=share * price
        rate=(money-capital)/capital
        result=dict(zip(["capital","money","rate","bonus"],\
                        [capital,money,rate,money-capital]))
        return result

    def printinvestment(self,datestart="",dateend=""):
        if datestart=="":
            datestart=self.Datelist[0]
        if dateend == "":
            dateend = self.Datelist[-1]
        a=self.dataperiod(datestart,dateend)
        dates=a["date"]
        NAVs=a["NAV"]
        money=a["investmoney"]
        share=a["share"]
        datas=list(zip(dates,NAVs,money,share))
        pricestock=self.getstocklist()
        line=[]
        for i in datas:
            line=i+pricestock[i[0]]
            print("%s %.4f %.3f %.4f %.4f %.3f %.4f %.3f"%(line[0],line[1],line[2],line[3],line[4],line[5],line[6], \
                                                    line[1]/line[4]-1))

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

    def investstrategy03(self,datestart,dateend="",moneypiece=10,ratetarget=0.20,daysmin=10,factor=10,investmax=1000):
        """Set a bonus rate garget, in investing period, buy more share (factor * moneypiece) when
           price fall over average price. if indicated end date, it will calculate to that day and
           the ignore ratetarget
        """
        days = 0
        mydatelist=self.dataperiod(datestart,self.Datelist[-1])["date"]
        dateprevious=datestart
        for datetrade in mydatelist:
            days += 1
            if days > daysmin:
                if dateend == "":
                    if self.sell(datetrade)["rate"] >= ratetarget:
                        break
                if datetrade == dateend:
                    break
            #below codes are different from previous strategy
            self.buy(datetrade,moneypiece)
            pricecurrent=self.tableNAV[datetrade]  #calculate down rate
            if  pricecurrent < self.pricestock(): # it worth buy when trade price > stock price
                if pricecurrent <= 0.98*self.pricestock() and self.moneyinvested()<=investmax:
                    self.buy(datetrade,self.moneyinvested())
                elif pricecurrent < 0.98*self.pricestock():
                    self.buy(datetrade,moneypiece*factor)    # factor decide added investing
                elif pricecurrent < 0.96*self.pricestock():
                    self.buy(datetrade,investmax)
                else:
                    self.buy(datetrade,moneypiece)
                #self.buy(datetrade,self.moneyinvested()) #previous stock decide investing,need huge money.
        return datetrade
    
    def investstrategy04(self,datestart,dateend="",moneypiece=10,ratetarget=0.10):
        
        days = 0
        mydatelist=self.dataperiod(datestart,self.Datelist[-1])["date"]
        for datetrade in mydatelist:
            self.checkaccountbank(datetrade)
            days += 1
            if days > 10:                
                if dateend == "":
                    if self.sell(datetrade)["rate"] >= ratetarget:
                        break
            self.buy(datetrade,moneypiece)
            addedmoney=self.howmuchmoney(datetrade)
            self.buy(datetrade,addedmoney)
        return datetrade
    
    

    def testing(self,datestart,dateend=""):
        self.readfund(self.fundcode)
        self.splitdata(datestart)
##        dateend=self.investstrategy03(datestart,dateend=dateend,\
##                                      moneypiece=10,ratetarget=0.20,daysmin=10,factor=10,investmax=5000)
        dateend=self.investstrategy04(datestart,dateend=dateend)
        self.printinvestment()
        result=self.sell(dateend)
        
        print("capital: %.2f, money: %.2f, bouns: %.2f, rate: %.4f"% \
              (result["capital"],result["money"],result["bonus"],result["rate"]))
        return dateend

class Investmentitem(object):
    def __init__(self,fundcode,date,price,money):
        self.date=date
        self.price=price
        self.money=money
        self.fundcode=fundcode
        pass

    def getrate(self,pricecurrent):
        return pricecurrent/price-1
    def getbonus(self,pricecurrent):
        return money*self.getrate(pricecurrent)
    def combineinvestment(self,addeditem):
        #share=money/price
        moneytotal = self.money + addeditem.money
        pricecombine=moneytotal/(self.money/self.price+addeditem.money/addeditem.price)
        self.money=moneytotal
        self.price=pricecombine
    def getmiddleprice(self,pricecurrent):
        pricetarget=(self.price+pricecurrent)/2
        moneyadded=(self.money/self.price-self.money/pricetarget) \
                    /(1/pricetarget-1/pricecurrent)
        return moneyadded
        
    

#fundlist=["001593","000962","000961"]
##a=Investment("000962")
##start="2016-05-03"
##
##for i in range(1):
##    start=a.testing(start,"2015-12-23")
##    print(start)
##    a.clearaccountfund()


#if you want to make it as a module, remove below code's #
def main():
    a=Investmentitem("000962","2019-01-01",1.22,1000)
    c=a.getmiddleprice(1.02)
    print(c)
    b=Investmentitem("000962","2019-02-01",1.02,c)
    print(a.price)
    print(b.price)
    a.combineinvestment(b)
    print(a.price)
    pass

if __name__=="__main__":
    main()
