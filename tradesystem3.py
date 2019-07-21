#Author: QiZhenHua 20190721

import Investment
market=Investment.Marketfund("000962")
market.readfund()
rateave=(max(market.NAVlist)+min(market.NAVlist))/2
ratescope=max(market.NAVlist)/rateave-1
ratesellshort=ratescope*0.2
rateselllong=ratescope*0.6
ratebuy=ratescope*0.05
ratepulldown=ratescope*0.4
print("ratescope: %f, ratesellshort: %f, rateselllong: %f, ratebuy: %f, ratepulldown: %f "\
      %(ratescope,ratesellshort,rateselllong,ratebuy,ratepulldown))


ratesell = 0.01
ratebuy = -0.007
ratepulldown = -0.1

datestart="2017-05-01"
market.splitdata(datestart)

investunit=100.0  # Minimum share unit

listprice=market.NAVlist[:1]
listinvest=[investunit]

moneyinbank=-sum(listinvest)*listprice[0]
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
    
    listrate=list(map(lambda x:pricetoday/x-1,listprice))

    print("pricetoday:{},pricelast:{},pricebase:{},moneyinbank:{},bouns:{}".format(\
        pricetoday,pricelast,pricebase,round(moneyinbank,2),round(bonus,2)))
    print(market.Datelist[current],listprice)
    
    if pricetoday / pricelast - 1 < -0.0:                     # today worth buying

        if len(listprice) < 100 and pricetoday/pricebase-1 <= ratebuy:  #control base

            listprice.append(pricetoday)
            listinvest.append(investunit)
            moneyinbank -= investunit * pricetoday
            status=status + "-Store!-"
            
        if listprice != []:
            for i_rate in enumerate(listrate): #range(len(listratepshort)):
                if i_rate[1] <= ratepulldown:
                    moneyinbank -= pricetoday * listinvest[i_rate[0]]
                    listinvest[i_rate[0]] = 2 * listinvest[i_rate[0]]
                    listprice[i_rate[0]] = (pricetoday + listprice[i_rate[0]]) / 2  #just pull down 1/2
                                        
                    status = status + "-pulldown long term price-"

    if pricetoday / pricelast - 1 > 0.0:  #today worth selling
        tempprice = []
        tempinvest = []
        flag = 1
        listrate.reverse()
        listprice.reverse()
        listinvest.reverse()
        
        for i_rate in enumerate(listrate):
            if i_rate[1] >= ratesell and flag:
                moneyinbank += pricetoday * listinvest[i_rate[0]]
                bonus += listinvest[i_rate[0]] * (pricetoday - listprice[i_rate[0]])
                flag = 0
            else:
                tempprice.append(listprice[i_rate[0]])
                tempinvest.append(listinvest[i_rate[0]])
        
        tempprice.reverse()
        tempinvest.reverse()

        listprice ,listinvest = tempprice , tempinvest
        pricebase = pricetoday

    
    current += 1
    input()
