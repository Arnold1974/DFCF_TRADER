#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import re
import time,sys
import requests
import threading
#import winsound
from voice import playsound
import pandas as pd
import tushare
import log

class PriceQuotation(object):
    def __init__(self,stockcode='600000'):
        self.kill=0
        self.show=0
        self.stockcode=False
        self.result=False
        
        self.stop_loss_price=False
        self.target_profit_price=False
        
        self.thread_2 = threading.Thread(target=self.get_tushare_quote,name='Thread__Monitor__Price')
        self.thread_2.setDaemon(True)
        self.thread_2.start()

    #获取实时行情
    def get_tushare_quote(self):
        while True:
            if self.kill==1:
                #winsound.PlaySound('./wav/stop price monitor CN.wav',winsound.SND_ASYNC)
                playsound(mac_say='price monitor stopped',win_sound='./wav/stop price monitor CN.wav',frequency=600, duration=500)
                break
            if self.stockcode <> False:
                try:
                    self.result=tushare.get_realtime_quotes(self.stockcode)
                except Exception as e:
                    log.error(e)
                    time.sleep(.5)
                    continue
                self.show_tushare_price(self.result)
            time.sleep(.5)
    def show_tushare_price(self, quote):
        if self.show==1:
                sys.stdout.write("\r\033[1;45m[%s %s]  %s   %.2f   %.2f%%   %s\033[0m" % \
                             (quote['date'][0],
                              quote['time'][0],
                              quote['name'][0],
                              float(quote['price'][0]),
                              (float(quote['price'][0])-float(quote['pre_close'][0]))/float(quote['pre_close'][0])*100,
                              quote['volume'][0]))
                sys.stdout.flush()
    
 #-------------------------------华丽的分割线-------------------  
    def get_dfcf_quote(self):
        '''
        获取东方财富的实时行情数据
        '''
        self.s = requests.session()
        while True:
            if self.kill==1:
                #winsound.PlaySound('./wav/stop price monitor CN.wav',winsound.SND_ASYNC)
                break
            if self.stockcode <> False:
                params={
                        'id':self.stockcode,
                        'callback':'',#'jQuery18302588442438663068_1484803703313',
                        '_':'' # repr(time.time()).replace(".","")
                       }
                try:
                    quote=self.s.get('https://hsmarket.eastmoney.com/api/SHSZQuoteSnapshot',params = params)
                    
                except Exception:
                    #log.error('price quotation error!');time.sleep(1)
                    print 'price quotation error!';time.sleep(1)
                    continue
                self.result=eval(re.search(r'{.*}',quote.text).group())
                self.show_dfcf_price(self.result)
            time.sleep(1)      
    def show_dfcf_price(self, quote):
        if self.show==1:
            sys.stdout.write("\r    *%s %s: %s  %s" % \
                         (time.strftime("%Y-%m-%d %X"),\
                          quote['name'],\
                          quote['realtimequote']['currentPrice'],\
                          quote['realtimequote']['zdf']))
            
            sys.stdout.flush()


# -------------------获取历史数据-----------------------------------------------
    def get_yahoo_hist_data(self,stockcode='000001.ss',s_date='2017-01-01',e_date=time.strftime('%Y-%m-%d',time.localtime())):
        '''
        yahoo 的历史数据
        深市数据链接：http://table.finance.yahoo.com/table.csv?s=000001.sz
        上市数据链接：http://table.finance.yahoo.com/table.csv?s=600000.ss
        上证综指代码：000001.ss
        '''
        if stockcode.startswith(('6')) and not stockcode.endswith(('ss')):
            stockcode+='.ss'
        elif stockcode.startswith(('0','2','3')) and not stockcode.endswith(('ss')):
            stockcode+='.sz'
        else:
            stockcode=stockcode

        a,b,c=str(int(s_date[5:7])-1),s_date[8:10],s_date[0:4]
        d,e,f=str(int(e_date[5:7])-1),e_date[8:10],e_date[0:4]
        url='http://table.finance.yahoo.com/table.csv?s='+stockcode
        url+='&d='+d+'&e='+e+'&f='+f+'&g=d&a='+a+'&b='+b+'&c='+c+'&ignore=.csv' #注意：月份要比实际月份少 1 
        df= pd.read_csv(url)
        return df.sort_index(ascending=False)


    def get_tushare_hist_data(self,code='600898',s_date='2017-01-01',e_date=time.strftime('%Y-%m-%d',time.localtime())):
        '''
        tushare 的历史数据
        '''
        while True:
            try:
                return tushare.get_k_data(code,s_date,e_date)
            except Exception as e:
                print e
                continue;time.sleep(1)



    def get_holding_period_price(self,code,buy_day):
        '''
        tushare 的历史行情数据
        '''
        df=self.get_tushare_hist_data(code,buy_day)
        index=df[df['date']==buy_day].index[0] #获取购买日的行号
        stock_holding_price={}
        stock_holding_price['Open']=float(format(df.ix[index,'open'], '.2f'))#*(1-float(strategy.lowerIncome)/100)
        stock_holding_price['High']=df['high'].max()
        stock_holding_price['Low']=df['low'].min()
        '''
        while index in df['date'].index:
            if stoc_holding_period['High']<df.ix[index,'high']:
                stoc_holding_period['High']=df.ix[index,'high']
                print 'Highest Price Updated on:  %s' % df.ix[index,'date']
            index+=1
        print len(df['high']),      df['high'].max() 
        '''
        #print df
        #print stock_holding_price
        #print u'\n止损价格: {0:.2f}'.format(stock_holding_price['Stop_loss'])
        #print format(show_list[1], '.2f')        
        return stock_holding_price
if __name__=="__main__":
    '''
    df=PriceQuotation().get_yahoo_hist_data('600898','2017-02-01')
    index=df[df['Date']=='2017-02-10'].index[0]
    Open,High,Low=df.ix[index,'Open'],df.ix[index,'High'],df.ix[index,'Low']
    show_list=[]
    show_list.append(Open);show_list.append(High);show_list.append(Low)
    
    print df
    print index,show_list
    
    '''
    test=PriceQuotation()
    df=test.get_tushare_hist_data('600300','2017-02-01')
    index=df[df['date']=='2017-02-10'].index[0]
    Open,High,Low=df.ix[index,'open'],df['high'].max(),df['low'].min()
    show_list=[]
    show_list.append(Open);show_list.append(High);show_list.append(Low)
    print df
    print "\n购买日开盘价:%.2f 持股期间最高价:%.2f 持股期间最低价:%.2f"% (show_list[0],show_list[1],show_list[2])
    print '{0:.2f}'.format(show_list[1])
    print format(show_list[1], '.2f')
    test.get_holding_period_price('600300','2017-02-10')
    test.kill=1
