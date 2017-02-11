# -*- coding: utf-8 -*-

import re
import time,sys
import requests
import threading
import winsound
import log


class PriceQuotation(object):
    def __init__(self,stockcode='600000'):
        self.kill=0
        self.show=0
        self.stockcode=False
        self.result=False
        self.thread_2 = threading.Thread(target=self.getquote,name='Thread__Monitor__Price')
        self.thread_2.setDaemon(True)
        self.thread_2.start()

    #获取实时行情
    def getquote(self):
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