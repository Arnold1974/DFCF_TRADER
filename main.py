# -*- coding:utf-8 -*-


from log import logger as log
from strategy import Strategy
from trade import DFCF_Trader
import sys
import time

 #获取交易时间段
def get_trade_time():
    if  time.localtime().tm_wday in range(0,5) and \
        (time.localtime().tm_hour in range(10,15) or \
        time.localtime().tm_hour==9 and  time.localtime().tm_min in range(15,60)):
        sys.stdout.write ( '\r[%50s]' % 'Trade Time...')
        return True
    else:
        sys.stdout.write ( '\r[%50s]' % 'NOt Trade Time...')

    

if __name__=="__main__":
    strategy=Strategy("QUERY_4_DAYS")
    trader=DFCF_Trader()

    if trader.thread_1.isAlive()==False:
        trader.__init__()

    result=strategy.pickstock()
    log.info(u"即时选股: %s \n" % (result[0][1] if len(result)!=0 else "[]"))
    result= strategy.traceback()
    log.info("%s 选出: %s" % ((result["stockDate"], result["data"][0]["codeName"]) if result!=False else (" ","[]")))
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
            
            