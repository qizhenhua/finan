import Investment
market=Investment.Investment()
market.readfund()

datestart="2018-01-16"
market.splitdata(datestart)
listprice=market.NAVlist[:10]
listinvest=[]
moneyinbank=0.0
bonus=0.0
status="Do nothing!"



for i in range(10):
    listinvest.append(100.0)


current=10
pricebase=market.tableNAV[market.Datelist[current-1]]

while current<len(market.Datelist):
    status="do nothing!"
    
    today=market.Datelist[current]
    pricetoday=market.tableNAV[today]
    lastday=market.Datelist[current-1]
    pricelast=market.tableNAV[lastday]
    
    listrate=list(map(lambda x:pricetoday/x-1,listprice))
    ratemin=min(zip(listrate,range(len(listrate))))
    ratemax=max(zip(listrate,range(len(listrate))))
    
    print(pricetoday,pricelast)
    
    if pricetoday>pricelast:
        if ratemax[0]>0.05:
            listprice.pop(ratemax[1])
            money=listinvest.pop(ratemax[1])
            moneyinbank +=money
            bonus +=ratemax[0]*money
            status="Sell!"
    else:
        if ratemin[0]<-0.04:
            listprice[ratemin[1]]=2/(1/listprice[ratemin[1]]+1/pricetoday)
            money=listinvest[ratemin[1]]
            listinvest[ratemin[1]] += money
            moneyinbank -= money
            status="Buy!"
    if status == "do nothing!":
        if pricetoday/pricebase-1 < -0.01:
            listprice.append(pricetoday)
            listinvest.append(100.0)
            moneyinbank -= 100.0
            pricebase=pricetoday
            status="Store!"
        elif pricetoday > pricebase:
            pricebase=pricetoday

    current +=1
    print("today is %s---%s"%(today, status))
    print(listprice)
    print("you reback money: %.3f and bouns: %.3f"%(moneyinbank,bonus))
    input()




