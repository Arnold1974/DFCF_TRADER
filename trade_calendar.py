#-*- coding:utf-8 -*-
import pandas as pd
import json,time

class TradeCalendar(object):
    
    def __init__(self):
        test_day=time.strftime("%Y/%m/%d",time.localtime(time.time()+2550000))
        self.df= pd.read_csv(".\calendar\calendar.csv")
        #如果本地文件已过期，查不到数据，则网络更新
        if not test_day in list(self.df['calendarDate']):
            self.config=json.load(file("./config/strategy.json"))
            self.df= pd.read_csv(self.config["TRADE_CALENDAR_URL"])
            self.df.to_csv('.\calendar\calendar.csv')
            print '### calendar.csv updated ###'       

    def trade_calendar(self,buy_date,hold_days):
        '''
                交易日历
        isOpen=1是交易日，isOpen=0为休市
        '''
              
        #return pd.read_csv("http://218.244.146.57/static/calAll.csv")

        index=self.df[self.df['calendarDate']==buy_date].index[0]
        i=0
        while i< int(hold_days-1):
            index+=1
            if self.df.ix[index,'isOpen'] == 1:
                i+=1
        #print u"%s买入后, 应该卖出的第%d个交易日为: %s" % (buy_date, hold_days, self.df.ix[index, 'calendarDate'])   
        return self.df.ix[index, 'calendarDate']
    def trade_day(self):
        buy_date=time.strftime("%Y/%m/%d",time.localtime())
        return self.df.ix[list(self.df['calendarDate']).index(buy_date),'isOpen']        

     
    #获取交易时间段
    def trade_time(self):
        if  time.localtime().tm_wday in range(0,5) and \
            (time.localtime().tm_hour in range(10,15) or \
            time.localtime().tm_hour==9 and  time.localtime().tm_min in range(15,60)):
            return True
        else:
            return False
         
if __name__=="__main__":
    test=TradeCalendar()
    test.trade_calendar("2017/02/07",4)   
    print "Today is Openday...........: %s" % test.trade_day()    
    print "Now is Trade Time..........: %s" % test.trade_time()
    
    
