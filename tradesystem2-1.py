import Investment
market=Investment.Investment("000962")
market.readfund()
rateave=(max(market.NAVlist)+min(market.NAVlist))/2
ratescope=max(market.NAVlist)/rateave-1
ratesellshort=ratescope*0.2
rateselllong=ratescope*0.6
ratebuy=ratescope*0.05
ratepulldown=ratescope*0.4
print("ratescope: %f, ratesellshort: %f, rateselllong: %f, ratebuy: %f, ratepulldown: %f "\
      %(ratescope,ratesellshort,rateselllong,ratebuy,ratepulldown))


ratesellshortup = 0.06
ratesellshortlow=0.12
rateselllong = 0.20
ratebuy = -0.008
ratepulldown = -0.4

datestart="2019-01-01"
market.splitdata(datestart)

investunit=1000.0

listpriceshort=market.NAVlist[:1]
listinvestshort=[investunit]

listpricelong=[]
listinvestlong=[]

moneyinbank=-sum(listinvestshort)
bonus=0.0

status="Do nothing!"

current=1
pricebase=market.tableNAV[market.Datelist[current]]

while current<len(market.Datelist):
    status=""
    
    today=market.Datelist[current]
    pricetoday=market.tableNAV[today]
    lastday=market.Datelist[current-1]
    pricelast=market.tableNAV[lastday]
    
    listrateshort=list(map(lambda x:pricetoday/x-1,listpriceshort))
    listrateshort=list(zip(listrateshort,range(len(listrateshort))))

    if listpricelong != []:
        listratelong=list(map(lambda x:pricetoday/x-1,listpricelong))
        listratelong=list(zip(listratelong,range(len(listratelong))))
        #ratelongmax=max(zip(listratelong,range(len(listratelong))))
    
    print(pricetoday,pricelast,pricebase)
    
    if pricetoday/pricelast-1 > 0: # sell
        if listpriceshort != []:
            indexremove=[]
            for i in range(len(listrateshort)):
                if (listrateshort[i][0]>ratesellshort*0.3 and listrateshort[i][0] <= ratesellshortup) or listrateshort[i][0] > ratesellshortlow:
                    listpriceshort[listrateshort[i][1]]
                    money=listinvestshort[listrateshort[i][1]]
                    moneyinbank += money
                    bonus += listrateshort[i][0] * money
                    status = status + "-Get short bonus!-"
                    indexremove.append(i)
                    
            if indexremove != []:
                indexremove.reverse()
                print(indexremove)
                for i in indexremove:
                    listpriceshort.pop(i)
                    listinvestshort.pop(i)
            

        if listpricelong != []:
            indexremove=[]
            for i in range(len(listratelong)):
                if listratelong[i][0] >= rateselllong:
                    listpricelong[listratelong[i][1]]
                    money = listinvestlong[listratelong[i][1]]
                    moneyinbank += money
                    bonus += listratelong[i][0] * money
                    status = status + "-Get long bonus!-"
                    indexremove.append(i)
            if indexremove != []:
                indexremove.reverse()
                print(indexremove)
                for i in indexremove:
                    listpricelong.pop(i)
                    listinvestlong.pop(i)

    elif pricetoday/pricebase-1 < -0.0:                     # buy

        if len(listpricelong)+len(listpriceshort) < 100 and pricetoday/pricebase-1 <= ratebuy:  #control base

            listpriceshort.append(pricetoday)
            listinvestshort.append(investunit)
            moneyinbank -= investunit
            status=status + "-Store!-"
            
        if listpricelong != []:
            for i in range(len(listratelong)):
                if listratelong[i][0] <= ratepulldown:
                    listpricelong[listratelong[i][1]] = 2/(1/listpricelong[listratelong[i][1]] + 1/pricetoday) #combine
                    money=listinvestlong[listratelong[i][1]]
                    listinvestlong[listratelong[i][1]] += money
                    moneyinbank -= money
                    status = status + "-pulldown long term!-"
                    
        if listpriceshort != []:
            indexremove=[]
            for i in range(len(listrateshort)):
                if listrateshort[i][0] <= ratepulldown:
                    listpriceshort[listrateshort[i][1]] = 2/(1/listpriceshort[listrateshort[i][1]] + 1/pricetoday)
                    money = listinvestshort[listrateshort[i][1]]
                    listinvestshort[listrateshort[i][1]] += money
                    moneyinbank -= money
                    status = status + "-Invest long term!-"
                    
                    listpricelong.append(listpriceshort[listrateshort[i][1]]) #if operate pulldown, it belong long term
                    listinvestlong.append(listinvestshort[listrateshort[i][1]])
                    indexremove.append(i)
            if indexremove != []:
                indexremove.reverse()
                print(indexremove)
                for i in indexremove:
                    listpriceshort.pop(i)
                    listinvestshort.pop(i)
    if pricetoday>pricelast :
            pricebase=pricetoday
                    
            
    current +=1
    print("today is %s---%s"%(today, status))
##    print("short:",listpriceshort)
##    print("long :",listpricelong)
    print("you reback money: %.3f and bouns: %.3f"%(moneyinbank,bonus))
    input()
