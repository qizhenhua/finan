import Investment
market=Investment.Investment("000962")
market.readfund()
rateave=(max(market.NAVlist)+min(market.NAVlist))/2
ratescope1=max(market.NAVlist)/rateave-1
ratescope2=min(market.NAVlist)/rateave-1
print(ratescope1,ratescope2)

datestart="2017-04-30"
market.splitdata(datestart)

listpriceshort=market.NAVlist[:1]
listinvestshort=[100.0]

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
                if listrateshort[i][0] >= 0.025:
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
                if listratelong[i][0] >= 0.2:
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

    elif pricetoday/pricebase-1 < -0.015:                     # buy

        if len(listpricelong)+len(listpriceshort) < 50:  #control base

            listpriceshort.append(pricetoday)
            listinvestshort.append(100.0)
            moneyinbank -= 100.0
##            pricebase=pricetoday
            status=status + "-Store!-"
            
        if listpricelong != []:
            for i in range(len(listratelong)):
                if listratelong[i][0] <= -0.10:
                    listpricelong[listratelong[i][1]] = 2/(1/listpricelong[listratelong[i][1]] + 1/pricetoday) #combine
                    money=listinvestlong[listratelong[i][1]]
                    listinvestlong[listratelong[i][1]] += money
                    moneyinbank -= money
                    status = status + "-pulldown long term!-"
                    
        if listpriceshort != []:
            indexremove=[]
            for i in range(len(listrateshort)):
                if listrateshort[i][0] <= -0.10:
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
