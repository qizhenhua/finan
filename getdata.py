# www.uqer.io
# login and "start research"

fundlist=["000961","001593"]  # Put fundation list in this list
for mychoice in fundlist:
    df=DataAPI.FundNavGet(secID=u"",ticker=mychoice,dataDate=u"",beginDate=u"20160101",endDate=u"",field=u"endDate,NAV",pandas="1")
    df.to_csv(mychoice+".csv",cloumns="",encoding="GBK")
