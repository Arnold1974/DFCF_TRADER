# -*- coding:utf-8 -*-

import log
#from log import logger as log
from strategy import Strategy
from trade import DFCF_Trader
from trade_calendar import TradeCalendar
import sys
import time

strategy=Strategy("QUERY_4_DAYS")
trader=DFCF_Trader()
calendar=TradeCalendar()

def monitor():
    result=strategy.pickstock()
    log.info(u"即时选股: %s " % (result[0][1] if len(result)!=0 else "[]"))
    result= strategy.traceback()
    log.info(u"[%s]选出:%s\n" % ((result["stockDate"], result["data"][0]["codeName"]) if result!=False else (" ","[]")))
    r=strategy.transaction()
    if r is not False:
        for i in xrange(len(r)):        
            result=r[i]
            print "%s %s %8s %s %s %s" % (result["stock_name"], \
                  result["bought_at"], result["sold_at"], \
                  result["buying_price"],result["selling_price"], \
                  result["signal_return_rate"])   
    while True:   
        if trader.login_flag==True:
            sys.stdout.write("\r[Time]: %10s \t [Thread-active]: %s" % (time.strftime("%Y-%m-%d %X",time.localtime()),trader.thread_1.isAlive()))
            time.sleep(1)
            
            
def run():

    if trader.thread_1.isAlive()==False:
        trader.__init__()

    while True:
        # 是否开市的日期
        if not calendar.trade_day():
            print "NONE TRADE DAY"
            time.sleep(1)
            continue
        elif not calendar.trade_time():
            print "NONE Trade time"
            time.sleep(1)
            continue
        else:
            #monitor
            print 'trade time'
            time.sleep(.5)

if __name__=="__main__":
    run()            