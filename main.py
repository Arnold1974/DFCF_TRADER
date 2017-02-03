# -*- coding:utf-8 -*-

import log
#from log import logger as log
from strategy import Strategy
from trade import DFCF_Trader
from trade_calendar import TradeCalendar
import sys
import time
import pandas as pd

strategy=Strategy("QUERY_4_DAYS")
time.sleep(.5)
trader=DFCF_Trader()
calendar=TradeCalendar()


            
def none_trade_day():
    if trader.login_flag==True:
        assets=trader.getassets()
        if assets:
            assets.update(trader.login_message['Data'][0])
            sys.stdout.write( "\r%(khmc)s [%(Syspm1)s]\tLogged at: [%(Date)s-%(Time)s] \
                                **************************************************** \
                               总资产:%(Zzc)s\t可用资金:%(Kyzj)s\t可取资金:%(Kqzj)s\t \
                               冻结资金:%(Djzj)s\t资金余额: %(Zjye)s \t总市值: %(Zxsz)s " % assets)
            sys.stdout.flush()
        df=pd.DataFrame(trader.login_message['Data'])            
        df=df.ix[:,[0,5,1,6]]
        df.columns = ['Date', 'Time','Account','Name']       
        #print user.login_message['Data']
        #print "qiwsir is in %(khmc)r"%user.login_message['Data']
        #sys.stdout.write( "\r %(khmc)s <%(Syspm1)s> Logged at: %(Date)s-%(Time)s "  \
        #                  % user.login_message['Data'][0])
    while not calendar.trade_day():
        #sys.stdout.write("\r "+time.ctime())
        time.sleep(1)           

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

def thread_login_keep_alive():
    if trader.thread_1.isAlive()==False:
        trader.__init__()
        time.sleep(2)    

def run():
    while trader.login_flag<>True:
        time.sleep(.5)

    while True:
        # 是否开市的日期
        if not calendar.trade_day():
            print '\n{0:-^60}'.format('NONE TRADE DAY')
            none_trade_day()
            time.sleep(1)
            continue
        elif not calendar.trade_time():
            print "Trade day, NONE Trade time"
            time.sleep(1)
            continue
        else: #进入交易时间
            print 'trade time'
            monitor()
            time.sleep(.5)

if __name__=="__main__":
    run()            