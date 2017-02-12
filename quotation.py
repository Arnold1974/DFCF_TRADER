# -*- coding: utf-8 -*-

import re
import time,sys
import requests
import threading
import winsound
import log
import pandas as pd

class PriceQuotation(object):
    def __init__(self,stockcode='600000'):
        self.kill=0
        self.show=0
        self.stockcode=False
        self.result=False
        self.thread_2 = threading.Thread(target=self.get_quote,name='Thread__Monitor__Price')
        self.thread_2.setDaemon(True)
        self.thread_2.start()

    #获取实时行情
    def get_quote(self):
        self.s = requests.session()
        while True:
            if self.kill==1:
                winsound.PlaySound('./wav/stop price monitor CN.wav',winsound.SND_ASYNC)
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
                    log.error('price quotation error!');time.sleep(1)
                    continue
                self.result=eval(re.search(r'{.*}',quote.text).group())
                self.show_price(self.result)
            time.sleep(1)

      
    def show_price(self, quote):
        if self.show==True:
            sys.stdout.write("\r    *%s %s: %s  %s" % \
                         (time.strftime("%Y-%m-%d %X"),\
                          quote['name'],\
                          quote['realtimequote']['currentPrice'],\
                          quote['realtimequote']['zdf']))
            

    def get_hist_price(self,stockcode='000001.ss',s_date='2017-01-01',e_date=time.strftime('%Y-%m-%d',time.localtime())):
        '''
        深市数据链接：http://table.finance.yahoo.com/table.csv?s=000001.sz
        上市数据链接：http://table.finance.yahoo.com/table.csv?s=600000.ss
        上证综指代码：000001.ss，深证成指代码：399001.SZ，沪深300代码：000300.ss
        '''
        if stockcode.startswith(('6')) and not stockcode.endswith(('ss')):
            stockcode+='.ss'
        elif stockcode.startswith(('0','2','3')) and not stockcode.endswith(('ss')):
            stockcode+='.sz'
        else:
            stockcode=stockcode

        print stockcode
        a,b,c=str(int(s_date[5:7])-1),s_date[8:10],s_date[0:4]
        d,e,f=str(int(e_date[5:7])-1),e_date[8:10],e_date[0:4]
        url='http://table.finance.yahoo.com/table.csv?s='+stockcode
        url+='&d='+d+'&e='+e+'&f='+f+'&g=d&a='+a+'&b='+b+'&c='+c+'&ignore=.csv' #注意：月份要比实际月份少 1 
        df= pd.read_csv(url)
        return df
if __name__=="__main__":
    result=PriceQuotation().get_hist_price('600898','2017-02-01')
    print result