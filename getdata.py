mychoice="519019"
df=DataAPI.FundNavGet(secID=u"",ticker=mychoice,dataDate=u"",beginDate=u"20160101",endDate=u"20190430",field=u"NAV",pandas="1")
df.to_csv(mychoice+".csv",cloumns="",encoding="GBK")
