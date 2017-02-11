# -*- coding:utf-8 -*-

import log
#from log import logger as log
from strategy import Strategy
from trade import DFCF_Trader
from trade_calendar import TradeCalendar
from quotation import PriceQuotation
import sys
import time
import pandas as pd
import winsound


def thread_login_keep_alive():
    if trader.thread_1.isAlive()==False:
        trader.__init__()
        time.sleep(2)  

def show_assets():
    assets=trader.getassets()
    if assets:
        assets.update(trader.login_message['Data'][0])
        print '\033[1;36m'
        print "%(khmc)s [%(Syspm1)s]\t    Logged at: [%(Date)s-%(Time)s]" % assets
        print '{0:-^60}'.format('')
        print "总资产: %(Zzc)10s\t可用资金: %(Kyzj)9s\t 可取资金: %(Kqzj)9s" % assets
        print "总市值: %(Zxsz)10s\t冻结资金: %(Djzj)9s\t 资金余额: %(Zjye)9s" % assets
        print '{0:-^60}'.format('')
        print '\033[0m'

def show_stocklist():
    stocklist=trader.getstocklist()
    if len(stocklist)==0:
        print u"\033[1;35m=== 空仓 ===\033[0m\n"
        return False
    else:
        for i in xrange(len(stocklist)):
            #转换盈亏比例为2位浮点百分小数
            stocklist[i]['Ykbl']=str(float('%.2f' % (float(stocklist[i]['Ykbl'])*100)))+'%'
            print '持仓:%(Zqmc)s  可用数量:%(Kysl)s  盈亏比例:%(Ykbl)s  累计盈亏:%(Ljyk)s' % stocklist[i]
        st=time.strftime("%Y-%m-%d",time.localtime(time.time()-864000))
        et=time.strftime("%Y-%m-%d",time.localtime(time.time()))
        hisdealdata=trader.gethisdealdata(st=st,et=et)
        todaydealdata=trader.gettodaydealdata()
        if len(todaydealdata)!=0:
            if todaydealdata[-1]['Zqmc']==stocklist[i]['Zqmc'] and todaydealdata[-1]['Mmlb_bs']=='B':
                buy_date=todaydealdata[-1]['Cjrq']
                buy_date='%s%s%s%s/%s%s/%s%s' % tuple(list(buy_date))
                for j in xrange(int(strategy.hold_days)):
                    show=calendar.trade_calendar(buy_date,j+1)
                    if show==time.strftime('%Y/%m/%d',time.localtime()):
                        print '\033[2;43m %s \033[0m' % show,
                    else:
                        print show,
                print '\n\n'    
                #print '买入日: %s   卖出日: %s' % (buy_date, calendar.trade_calendar(buy_date,4))
                stocklist[i]['sell_day']=calendar.trade_calendar(buy_date,4) 

        elif len(hisdealdata)!=0:
            if hisdealdata[-1]['Zqmc']==stocklist[i]['Zqmc'] and hisdealdata[-1]['Mmlb_bs']=='B':
                buy_date=hisdealdata[-1]['Cjrq']
                buy_date='%s%s%s%s/%s%s/%s%s' % tuple(list(buy_date))
                
                for j in xrange(int(strategy.hold_days)):
                    show=calendar.trade_calendar(buy_date,j+1)
                    if show==time.strftime('%Y/%m/%d',time.localtime()):
                        print '\033[2;43m %s \033[0m' % show,
                    else:
                        print show,
                print '\n\n'    
                #print '买入日: %s   卖出日: %s' % (buy_date, calendar.trade_calendar(buy_date,4))
                stocklist[i]['sell_day']=calendar.trade_calendar(buy_date,4)               
    return stocklist[i]
           
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
    print '\n\n{0:-^72}'.format('\033[20;43m NON TRADING DAY \033[0m')    
    show_assets()
    show_stocklist()
    quotation.stockcode=False
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
    print '\n{0:-^72}'.format('\033[20;46m NON TRADING TIME \033[0m')    
    show_assets()
    show_stocklist()
    quotation.stockcode=False
    while not calendar.trade_time() and calendar.trade_day():
        if int(time.time()) % 2:
             sys.stdout.write("\r[%s] %s" % (time.strftime("%X",time.localtime()),"--> Non Trading Time !"))           
        else:
             sys.stdout.write("\r[%s] %s" % (time.strftime("%X",time.localtime()),"-->                   "))
        time.sleep(1)
    
def monitor_buy(code,codename):
    quotation.stockcode=code
    quotation.show=True 
    while calendar.trade_time() and calendar.trade_day():
        if float(quotation.result['realtimequote']['currentPrice'])>10.80 \
           and float(quotation.result['realtimequote']['zdf'].replace('%',''))>-9 \
           and time.localtime()[3:5]>=(9,26):
            print "Begin Buy: " + codename
            trader.deal(code,codename,quotation.result['fivequote']['sale5'],'B')
            #trader.deal("000619","海螺型材","13.4","B")            
            winsound.PlaySound('./wav/transaction completed.wav',winsound.SND_ASYNC)
            return
                

def monitor_sell(code,sell_day,stock_amount):
    '''
    如果选出的股票在下一个交易日出现停牌、开盘涨跌幅小于-9%、一字板涨跌停、 则取消买入这只股票
    上涨后回撤止盈: 持股期内当收益率触发止盈条件时(某交易日时点出现即触发，而不是收盘价），
    当日便不卖出，而是等下个交易日出现止盈回撤条件触发。
    例如：本来持有4天卖出的股票，
    但是到了第3天，某时点出现收益21%(用户设定的止盈条件是大于20%时，回撤5%止盈)，则当天会继续持有，
    到期也不卖出了。当该股收益最高点出现后，从次日起只要收益从最高点回撤大于5%时就会卖出止盈。

    特殊情况：当持有股票一字涨跌停时，会继续持有。

    result=strategy.pickstock()
    log.info(u"即时选股: %s " % (result[0][1] if len(result)!=0 else "[]"))
    result= strategy.traceback()
    log.info(u"[%s]回测选股:%s\n" % ((result["stockDate"], result["data"][0]["codeName"]) if result!=False else (" ","[]")))
    '''
    quotation.stockcode=code
    quotation.show=1
    while calendar.trade_time() and calendar.trade_day():       
       #卖出条件触发，发卖出指令
       if int(stock_amount)<>0 and float(quotation.result['realtimequote']['currentPrice'])>30.80 \
          or sell_day==time.strftime("%Y/%m/%d",time.localtime(time.time())) and time.localtime()[3:5]==(14,58):
            print '\n\nBegin Sell'
            #trader.deal(code,quote['name'],quote['bottomprice'],'S')
            print 'Sell completed\n'
            stock_amount=show_stocklist()['Kysl']
       time.sleep(1)

def trade_time():
    print '\n{0:-^72}'.format('\033[20;43m TRADING TIME \033[0m')
    show_transaction(start_day='2017-01-01', end_day='2017-12-31')
    show_assets()
    stock_in_position=show_stocklist()

    if stock_in_position: #如果不空仓，监视价格变化是否达到止损止盈
        print 'Monitor Sell Condition:'
        monitor_sell(stock_in_position['Zqdm'],stock_in_position['sell_day'],stock_in_position['Kysl'])
    else:  #position is empty, 需要开仓
        result= strategy.traceback()
        if result==False: #没有选出目标
            print 'Selected Stock: None! Keep Position 0\n'
            while calendar.trade_time() and calendar.trade_day():
                if int(time.time()) % 2:
                     sys.stdout.write("\r[%s] %s" % (time.strftime("%X",time.localtime()),"--> No Trade Target !"))           
                else:
                     sys.stdout.write("\r[%s] %s" % (time.strftime("%X",time.localtime()),"-->                  "))
                time.sleep(1)                
        else: #选出目标， 开仓
            code=result["data"][0]["code"]
            codename= result["data"][0]["codeName"]
            print "%s:[%s] ---> 购买日:%s\n" %((result["stockDate"], result["data"][0]["codeName"],calendar.trade_calendar(result["stockDate"].replace("-","/"),2)) if result!=False else (" ","[]"," "))
            #log.info(u"[%s]选出:%s\n" % ((result["stockDate"], result["data"][0]["codeName"]) if result!=False else (" ","[]")))
            quote=trader.getquote(code)       
            print quote['name'],quote['code'],quote['topprice'],quote['bottomprice'],\
                  quote['realtimequote']['open'],quote['realtimequote']['time'],\
                  quote['realtimequote']['currentPrice'],\
                  quote['realtimequote']['zd'],\
                  quote['realtimequote']['zdf'],\
                  quote['fivequote']['buy1'],\
                  quote['fivequote']['sale1']

            monitor_buy(code,codename)
            show_stocklist()
            while calendar.trade_time() and calendar.trade_day():
                time.sleep(1)        
            quotation.kill=1        
#----------------------------------------------------------------------------------------------
def run():
    while trader.login_flag<>True:
        time.sleep(1)


    while True:
        # 是否交易的日期
        if not calendar.trade_day():
            none_trade_day()
            continue
        elif not calendar.trade_time(): #交易日非交易时间段
            none_trade_time()
            continue
        else: #进入交易时间  calendar.trade_day() & calendar.trade_time()
            trade_time()
            #time.sleep(.5)
              
if __name__=="__main__":    
    strategy=Strategy("QUERY_2_DAYS",25,5,10)
    time.sleep(.5)
    trader=DFCF_Trader()
    calendar=TradeCalendar()
    quotation=PriceQuotation()
    try:
        run()
    except KeyboardInterrupt:
        #关闭打开的线程
        trader.kill=1
        quotation.kill=1
        print '\n\nCtrl-C Entered'