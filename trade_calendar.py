#-*- coding:utf-8 -*-
import pandas as pd

class TradeCalendar(object):

    def trade_calendar(self,buy_date,hold_days):
        '''
                交易日历
        isOpen=1是交易日，isOpen=0为休市
        '''

        self.config=json.load(file("./config/strategy.json"))
        df= pd.read_csv(self.config["TRADE_CALENDAR_URL"])
        print df.ix[list(df['calendarDate']).index(buy_date),'isOpen']        
        
        #return pd.read_csv("http://218.244.146.57/static/calAll.csv")

        index=df[df['calendarDate']==buy_date].index[0]
        i=0
        while i< int(hold_days-1):
            index+=1
            if df.ix[index,'isOpen'] == 1:
                i+=1
        print u"%s买入后, 应该卖出的第%d个交易日为: %s" % (buy_date, hold_days, df.ix[index, 'calendarDate'])   
`