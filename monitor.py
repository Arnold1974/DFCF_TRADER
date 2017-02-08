# -*- coding: utf-8 -*-

import re
import time,sys
import requests
import threading

class Monitor(object):
    def __init__(self,stockcode):
        self.thread_2 = threading.Thread(target=self.getquote,name='Thread__Monitor__Price')
        self.thread_2.setDaemon(True)
        self.thread_2.start()
        self.stockcode=stockcode
        self.show=0
        self.kill=0
    #获取实时行情
    def getquote(self):
        self.s = requests.session()
        while True:
            if self.kill==True:
                break
            params={
                    'id':self.stockcode,
                    'callback':'',#'jQuery18302588442438663068_1484803703313',
                    '_':'' # repr(time.time()).replace(".","")
                   }
            try:
                quote=self.s.get('https://hsmarket.eastmoney.com/api/SHSZQuoteSnapshot',params = params)
                
            except Exception as e:
                print e;time.sleep(1)
                continue
            self.result=eval(re.search(r'{.*}',quote.text).group())
            self.price_monitor(self.result)
            time.sleep(1)

      
    def price_monitor(self, quote):
        if self.show==True:
            sys.stdout.write("\r%s %s: %s  %s" % \
                         (time.strftime("%Y-%m-%d %X"),\
                          quote['name'],\
                          quote['realtimequote']['currentPrice'],\
                          quote['realtimequote']['zdf']))          