# -*- coding:utf-8 -*-

import log
#from log import logger as log
from strategy import Strategy
from trade import DFCF_Trader
from trade_calendar import TradeCalendar
import sys
import time
import pandas as pd
import winsound

strategy=Strategy("QUERY_4_DAYS")
time.sleep(.5)
trader=DFCF_Trader()
calendar=TradeCalendar()

def thread_login_keep_alive():
    if trader.thread_1.isAlive()==False:
        trader.__init__()
        time.sleep(2)  

def show_assets():
    assets=trader.getassets()
    if assets:
        assets.update(trader.login_message['Data'][0])
        print '\033[1;36m'
        print "\n%(khmc)s [%(Syspm1)s]\t    Logged at: [%(Date)s-%(Time)s]" % assets
        print '{0:-^60}'.format('')
        print "总资产: %(Zzc)10s\t可用资金: %(Kyzj)9s\t 可取资金: %(Kqzj)9s" % assets
        print "总市值: %(Zxsz)10s\t冻结资金: %(Djzj)9s\t 资金余额: %(Zjye)9s" % assets
        print '{0:-^60}'.format('')
        print '\033[0m'

def show_stocklist():
    stocklist=trader.getstocklist()
    if len(stocklist)==0:
        print "\033[1;35mStock Position:  0 \033[0m\n"
        return False
    else:
        for i in xrange(len(stocklist)):
            print '%(Zqmc)s 可用数量:%(Kysl)s 盈亏比例:%(Ykbl)s 累计盈亏:%(Ljyk)s' % stocklist[i]
        for i in xrange(len(trader.gethisdealdata())):
            print trader.gethisdealdata()[i]
                
def show_transaction(start_day='2015-01-01', end_day='2017-12-31'):
    r=strategy.transaction(start_day,end_day)
    print '\n{0:-^60}'.format('Portfolie Value ')
    if r is not False:
        portfolio=1
        for i in xrange(len(r)-1,-1,-1):
            result=r[i]
            print "%s  %s %8s  %6s %6s %6s   %1.3f" % (result["stock_name"], \
                  result["bought_at"], result["sold_at"], \
                  result["buying_price"],result["selling_price"], \
                  result["signal_return_rate"], \
                  (1+float(result["signal_return_rate"])/100)*portfolio)                       
            portfolio *= 1+float(result["signal_return_rate"])/100    

def none_trade_day():
    print '\n\n{0:-^72}'.format('\033[20;43mNONE TRADE DAY\033[0m')    
    show_assets()
    show_stocklist()
        #df=pd.DataFrame(trader.login_message['Data'])            
        #df=df.ix[:,[0,5,1,6]]
        #df.columns = ['Date', 'Time','Account','Name']       
        #print user.login_message['Data']
        #print "qiwsir is in %(khmc)r"%user.login_message['Data']
        #sys.stdout.write( "\r %(khmc)s <%(Syspm1)s> Logged at: %(Date)s-%(Time)s "  \
        #                  % user.login_message['Data'][0])
        #sys.stdout.flush()       

    while not calendar.trade_day():
        if int(time.time()) % 2:
             sys.stdout.write("\r\033[1;43m[%s]  Login-Thread Alive: %s\033[0m" % (time.strftime("%X",time.localtime()),trader.thread_1.isAlive()))          
        else:
             sys.stdout.write("\r[%s]" % (time.strftime("%X",time.localtime())))
        time.sleep(1)           

def none_trade_time():
    print '\n\n{0:-^72}'.format('\033[20;46mNONE TRADE TIME\033[0m')    
    show_assets()
    show_stocklist()
    while not calendar.trade_time():
        if int(time.time()) % 2:
             sys.stdout.write("\r[%s] %s" % (time.strftime("%X",time.localtime()),"--> None Trade Time !"))           
        else:
             sys.stdout.write("\r[%s] %s" % (time.strftime("%X",time.localtime()),"-->                  "))
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

def trade_time():
    print '\n\n{0:-^72}'.format('\033[20;43mTRADE TIME\033[0m')
    show_transaction(start_day='2017-01-01', end_day='2017-12-31')
    show_assets()  
    
    result= strategy.traceback()
    if result==False:
        print 'Select None'
    else:
        code=result["data"][0]["code"]
        codename= result["data"][0]["codeName"]

        show_stocklist()
        
        print "%s选出:%s ---> 购买日:%s\n" %((result["stockDate"], result["data"][0]["codeName"],calendar.trade_calendar(result["stockDate"].replace("-","/"),2)) if result!=False else (" ","[]"," "))
        #log.info(u"[%s]选出:%s\n" % ((result["stockDate"], result["data"][0]["codeName"]) if result!=False else (" ","[]")))
        
        quote=trader.getquote(code)       
        print quote['name'],quote['code'],quote['topprice'],quote['bottomprice'],\
              quote['realtimequote']['open'],quote['realtimequote']['time'],\
              quote['realtimequote']['currentPrice'],\
              quote['realtimequote']['zd'],\
              quote['realtimequote']['zdf'],\
              quote['fivequote']['buy1'],\
              quote['fivequote']['sale1']
          
  
    if result!=False:
        print "Begin Buy: " + codename
        winsound.PlaySound('./wav/transaction completed.wav',winsound.SND_ASYNC)
        #trader.deal(code,codename,quote['fivequote']['sale5'],'B')
        #trader.deal("000619","海螺型材","13.4","B")
        while calendar.trade_time():
            quote=trader.getquote(code)
            sys.stdout.write("\r%s %s: %s  %s" % \
                             (time.strftime("%Y-%m-%d %X"),\
                              quote['name'],\
                              quote['realtimequote']['currentPrice'],\
                              quote['realtimequote']['zdf']))
            time.sleep(1)        
        
#----------------------------------------------------------------------------------------------
def run():
    while trader.login_flag<>True:
        time.sleep(1)

    while True:
        # 是否开市的日期
        if not calendar.trade_day():
            none_trade_day()
            continue
        elif not calendar.trade_time():
            none_trade_time()
            continue
        else: #进入交易时间  calendar.trade_day() & calendar.trade_time()
            trade_time()
            #time.sleep(.5)
              
if __name__=="__main__":
    try:
        run()
    except KeyboardInterrupt:
        print '\n\nCtrl-C Entered'