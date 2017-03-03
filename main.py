#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import division
import log
#from log import logger as log
from strategy import Strategy
from trade import DFCF_Trader
from trade_calendar import TradeCalendar
from quotation import PriceQuotation
import sys
import time
import pandas as pd
#import winsound
from voice import playsound


def thread_login_keep_alive():
    if trader.thread_1.isAlive()==False:
        trader.__init__()
        time.sleep(2)

def show_assets():
    assets=trader.getassets()
    if assets:
        assets.update(trader.login_message['Data'][0])
        show= '\n\033[2;36m'+\
              "%(khmc)s [%(Syspm1)s]\t         Logged at: [%(Date)s - %(Time)s]\n" +\
              '{0:-^70}'.format('') +'\n'+\
              "总资产: %(Zzc)11s   可用资金: %(Kyzj)11s   可取资金: %(Kqzj)11s\n" +\
              "总市值: %(Zxsz)11s   冻结资金: %(Djzj)11s   资金余额: %(Zjye)11s\n" +\
              '{0:-^70}'.format('')+ '\033[0m'
        print show % assets
        ''' 
        print '\033[2;36m'
        print "%(khmc)s [%(Syspm1)s]\t    Logged at: [%(Date)s-%(Time)s]" % assets
        print '{0:-^60}'.format('')
        print "总资产: %(Zzc)10s\t可用资金: %(Kyzj)9s\t 可取资金: %(Kqzj)9s" % assets
        print "总市值: %(Zxsz)10s\t冻结资金: %(Djzj)9s\t 资金余额: %(Zjye)9s" % assets
        print '{0:-^60}'.format('')
        print '\033[0m'
        '''
def show_stocklist(): #获取持仓股票的买入日期，持仓数据中不显示，需从当日成交数据和历史成交数据中获取
    stocklist=trader.getstocklist()
    if len(stocklist)==0:
        print u"\033[1;35m=== 空仓 ===\033[0m\n"
        return False
    else:
        for i in xrange(len(stocklist)):
            #转换盈亏比例为2位浮点百分小数
            stocklist[i]['Ykbl']=str(float('%.2f' % (float(stocklist[i]['Ykbl'])*100)))+'%'
            stocklist[i]['Cwbl']=str('%.0f' % (float(stocklist[i]['Cwbl'])*100))+'%'
            print '\033[1;42m%(Zqmc)s ==> 持仓:%(Zqsl)4s 可用:%(Kysl)4s  仓位:%(Cwbl)3s  涨跌:%(Ykbl)5s  盈亏:%(Ljyk)8s\033[0m' % stocklist[i]
        st=time.strftime("%Y-%m-%d",time.localtime(time.time()-864000))
        et=time.strftime("%Y-%m-%d",time.localtime(time.time()))
        hisdealdata=trader.gethisdealdata(st=st,et=et)
        todaydealdata=trader.gettodaydealdata()
        show=[]
        if len(todaydealdata) <> 0 or len(hisdealdata) <> 0:
            dealdata=hisdealdata if len(todaydealdata)!=0 else hisdealdata
            if dealdata[-1]['Zqmc']==stocklist[i]['Zqmc'] and dealdata[-1]['Mmlb_bs']=='B':
                buy_date=dealdata[-1]['Cjrq']
                buy_date='%s%s%s%s/%s%s/%s%s' % tuple(list(buy_date))
                buy_date_for_return=buy_date.replace('/','-')

                print'     + + +'
                for j in xrange(int(strategy.hold_days)):
                    next_day=calendar.trade_calendar(buy_date,j+1)
                    show.append(next_day)
                
                #如果持股日期炒股策略最后期限，则显示到目前的状态
                while show[-1]<time.strftime('%Y/%m/%d',time.localtime()):
                    next_day=calendar.trade_calendar(next_day,2)
                    if next_day > time.strftime('%Y/%m/%d',time.localtime()):
                        #show.append('- - -')
                        show.append('\033[1;36m' + next_day + '\033[0m')
                        break
                    show.append(next_day)
               
                for L in xrange(len(show)):
                    if show[L]==calendar.trade_calendar(buy_date,int(strategy.hold_days)):
                       show[L]='\033[2;41m%s\033[0m' % show[L]                   
                    if show[L]==time.strftime('%Y/%m/%d',time.localtime()):
                        show[L]='\033[2;46m%s\033[0m' % show[L]
                    if ((L+1) % 6 <> 0):
                        print show[L].replace('/','-'),
                    else: 
                        print show[L].replace('/','-') 
                print '\n\n{0:=^70}'.format('')
                        
                #print '\n'+' '*13*(k) +'       ---->'
                #print '买入日: %s   卖出日: %s' % (buy_date, calendar.trade_calendar(buy_date,4))
                stocklist[i]['sell_day']=calendar.trade_calendar(buy_date,int(strategy.hold_days))
                stocklist[i]['buy_day']=buy_date_for_return

    return stocklist[i]

def show_transaction():
    start_day=time.strftime("%Y",time.localtime())+'-01-01'
    end_day=time.strftime("%Y-%m-%d",time.localtime())
    r=strategy.transaction(start_day,end_day)
    print '\n{0:*^70}'.format(' Portfolie Value ')
    if r is not False:
        portfolio=1
        for i in xrange(len(r)-1,-1,-1):
            result=r[i]
            if len(result["stock_name"])==3:
                result["stock_name"]=result["stock_name"]+'  '
            print "%s   %s   %8s    %6s  %6s  %6s    %1.3f" % (result["stock_name"], \
                  result["bought_at"], result["sold_at"], \
                  result["buying_price"],result["selling_price"], \
                  result["signal_return_rate"], \
                  (1+float(result["signal_return_rate"])/100)*portfolio)
            portfolio *= 1+float(result["signal_return_rate"])/100
        print '%s         --->   %s' % (result["stock_name"], calendar.trade_calendar(result["bought_at"].replace("-","/"),int(strategy.hold_days)))
    print '{0:*^70}\n'.format(' End of Show ')
def none_trade_day():
    quotation.kill=1
    quotation.stockcode=False
    quotation.resulult=False
    #show_assets()
    print '\n\n{0:=^81}'.format('\033[20;44m NON TRADING DAY \033[0m')
    show_transaction()
    show_assets()    
    
    stock_in_position = show_stocklist()
    if stock_in_position == False:
        result = strategy.traceback()
        if result != False:
            show = "\r%s 策略选股: %s [%s] ---> 购买日:%s" %((result["stockDate"], result["data"][0]["codeName"], \
                 result["data"][0]["code"], calendar.trade_calendar(result["stockDate"].replace("-","/"),2)))
        else:
            show = "\r策略选股: None"
    else: show = "\rLogin-Thread Alive: %s" % (trader.thread_1.isAlive(),)
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
            sys.stdout.write(show)
        else:
            sys.stdout.write('\033[1;44m'+ show + time.strftime("%X",time.localtime())+ '\033[0m')
        sys.stdout.flush()
        time.sleep(1)

def none_trade_time():
    quotation.kill=1
    quotation.stockcode=False
    quotation.resulult=False
    #show_assets()
    print '\n{0:=^81}'.format('\033[2;41m NON TRADING TIME \033[0m')
    show_transaction()
    show_assets()
    
    stock_in_position = show_stocklist()
    if stock_in_position == False:
        result = strategy.traceback()
        if result != False:
            show = "\r%s 策略选股: %s [%s] ---> 购买日:%s" %((result["stockDate"], result["data"][0]["codeName"], \
                 result["data"][0]["code"], calendar.trade_calendar(result["stockDate"].replace("-","/"),2)))
        else:
            show = "\r策略选股: None"
    else: show = "\rLogin-Thread Alive: %s" % (trader.thread_1.isAlive(),)
 
    while not calendar.trade_time() and calendar.trade_day():
        if int(time.time()) % 2:
            sys.stdout.write(show + "  ")
        else:
            sys.stdout.write('\033[1;41m'+ show + "  " + time.strftime("%X",time.localtime()) + '\033[0m')
        sys.stdout.flush()
        time.sleep(1)

        '''
        if int(time.time()) % 2:
            sys.stdout.write("\r\033[2;41m[%s] %s\033[0m" % (time.strftime("%X",time.localtime()),"--> Non Trading Time !"))
        else:
            sys.stdout.write("\r[%s] %s" % (time.strftime("%X",time.localtime()),"-->                   "))
        sys.stdout.flush()
        time.sleep(1)
        '''
def monitor_buy(code,codename):
    print '=== Monitor Price for Buy: %s ===' % code
    quotation.stockcode=code

    while quotation.result is False:
        time.sleep(.5)

    dfcf_quote=trader.getquote(code) #获取东方财富的报价：涨跌停价格不需要即时报价
    print u'跌停价:{0:s} | 涨停价:{1:s}'.format(dfcf_quote['bottomprice'],dfcf_quote['topprice'])

    quotation.show=1
    while calendar.trade_time() and calendar.trade_day():
        buy_condition_0 = quotation.result['code'][0]==code
        buy_condition_1 = (float(quotation.result['price'][0])-float(quotation.result['pre_close'][0]))*100/float(quotation.result['pre_close'][0])>-9
        buy_condition_2 = time.localtime()[3:6]>=(9,25,30) and time.localtime()[3:6]<=(9,40,6)
     
        if buy_condition_0 and buy_condition_1 and buy_condition_2:
            if float(quotation.result['open'][0]) == float(quotation.result['amount'][0]) ==0:
                print "\n%s %s: Suspension\n" % (quotation.result['date'][0],codename)
                while calendar.trade_time() and calendar.trade_day():
                    time.sleep(2)
            quotation.show=0
            print '\n'
            log.info("Begin Buy -->  %s" % codename)
            Wtbh=trader.deal(code,codename,str(float(dfcf_quote['topprice'])-0.01),'B') #['topprice']

            if Wtbh is not None:
                log.info('Buy Order Accomplished!')
                #os.system("say order completed")
                #winsound.PlaySound('./wav/transaction completed.wav',winsound.SND_ASYNC)
                playsound(mac_say='transaction completed',win_sound='./wav/transaction completed.wav',frequency=450, duration=150)
                #查询当日委托状态， 如果未成则等待
                while trader.getordersdata()[-1]['Wtzt'] <> '已成':
                    sys.stdout.write("\r委托编号:[%s] 还未成交!" % Wtbh)
                    sys.stdout.flush()
                    time.sleep(5)
                log.info('Deal Done!')
                #return Wtbh             
                #按照涨停价-0.01挂单，如果成交价格为开盘价， 则还有10%的资金未利用        
                Wtbh_02 = None
                if round(float(quotation.result['open'])*0.98,2)>=float(dfcf_quote['bottomprice']):
                    log.info("Begin Buy -->  %s %s" % (codename,format(float(quotation.result['open'])*0.98, '.2f')))
                    Wtbh_02=trader.deal(code,codename,format(float(quotation.result['open'])*0.98, '.2f'),'B')                
                    log.info('Deal Done!')
                #--------------------------------------------------------------------------    
                return Wtbh + " | " + Wtbh_02 if Wtbh_02 is not None else Wtbh
            else:
                return 'buy order failed!'
            
        '''
        if quotation.result['code']==code \
           and float(quotation.result['realtimequote']['currentPrice'])>10.80 \
           and float(quotation.result['realtimequote']['zdf'].replace('%',''))>-9 \
           and time.localtime()[3:5]>=(9,29) and time.localtime()[3:5]<=(9,31):
            print "Begin Buy: " + codename
            #Wtbh=trader.deal(code,codename,quotation.result['fivequote']['sale5'],'B') #['topprice']
            #trader.deal("000619","海螺型材","13.4","B")
            winsound.PlaySound('./wav/transaction completed.wav',winsound.SND_ASYNC)
            return Wtbh
        '''
        time.sleep(1)

             
def monitor_sell(code,buy_day,sell_day,stock_amount):
    '''
    如果选出的股票在下一个交易日出现停牌、开盘涨跌幅小于-9%、一字板涨跌停、 则取消买入这只股票
    上涨后回撤止盈: 持股期内当收益率触发止盈条件时(某交易日时点出现即触发，而不是收盘价），
    当日便不卖出，而是等下个交易日出现止盈回撤条件触发。
    例如：本来持有4天卖出的股票，
    但是到了第3天，某时点出现收益21%(用户设定的止盈条件是大于20%时，回撤5%止盈)，则当天会继续持有，
    到期也不卖出了。当该股收益最高点出现后，从次日起(当日不管是否出现回撤止盈)开始重新监测，
    只要收益从最高点回撤大于5%时就会卖出止盈。
    {目前建议采用的止盈策略，盘中出现持股期间股价新高后，更新止损价， 随时止损}

    特殊情况：当持有股票一字涨跌停时，会继续持有。
    '''
    print '\n\033[3;33m     === Monitor Price for Selling [%s]: ===\033[0m' % code
    quotation.stockcode=code
    
    while quotation.result is False:
        time.sleep(.5)

    stock_holding_price=quotation.get_holding_period_price(code,buy_day)
    stop_loss_price=stock_holding_price['Open'] * (1-float(strategy.lowerIncome)/100) #止损价格
    stop_sell_price=stock_holding_price['Open'] * (1+float(strategy.upperIncome)/100) #止盈价格
    price_updated=False # 判断是否出现新的价格高点， 用来处理到期卖出还是看回撤卖出
    if stock_holding_price['High'] > stop_sell_price:
        stop_sell_price=stock_holding_price['High'] #最新的止盈价格
        stop_loss_price=stop_sell_price * (1-float(strategy.fallIncome)/100) #最新的止损价格
        price_updated=True

    dfcf_quote=trader.getquote(code) #获取东方财富的报价：涨跌停价格不需要即时报价
    print u'止损价:{0:.2f} | 止盈价:{1:.2f} | 跌停价:{2:s} | 涨停价:{3:s}' \
          .format(stop_loss_price,stop_sell_price,dfcf_quote['bottomprice'],dfcf_quote['topprice'])
    #print '跌停价格: %s' % dfcf_quote['bottomprice']
    
    #卖出日，非一字涨停，如果涨停价也不能触及止盈价，则涨到 5% 就卖出，不用等收盘
    if sell_day <= time.strftime("%Y/%m/%d",time.localtime(time.time())) \
                   and price_updated <> True \
                   and float(dfcf_quote['topprice']) < stop_sell_price:
       print u'今日涨停价达不到止盈价, 因此盘中价格达到 4% 就卖出!' 

    quotation.show=1
    while calendar.trade_time() and calendar.trade_day() and int(stock_amount)<>0:
        if float(quotation.result['high'][0])>stop_sell_price:  #最新止盈价格出现，更新止盈价格，当日停止卖出
            price_updated=True
            quotation.show=0
            stop_sell_price=float(quotation.result['high'][0])
            stop_loss_price=stop_sell_price * (1-float(strategy.fallIncome)/100) #最新的止损价格    
            print 'The new highest price: %s occurred at: %s' % (stop_sell_price,time.strftime('%X' , time.localtime()))
            quotation.show=1
            
        #-----------卖出条件触发，发卖出指令-----------
        # .0. 确认是当前股票的报价，并且有仓位可用
        sell_condition_0 = quotation.result['code'][0]==code and int(stock_amount)<>0
        
        # .1. 触发止损 (用实时行情胡最低价与止损价格比较)
        sell_condition_1 = float(quotation.result['low'][0]) <= stop_loss_price  \
                         and time.localtime()[3:6]>=(9,30,1)

        # .2. 卖出日，没触及止盈点，并且不是一字涨停 (最低价不等于涨停价),收盘价卖出               
        #     sell_day 为策略理论卖出日，如果因其他原因该卖没卖， 则以后会出现sell_day < 当前日期
        #     而且止盈点也没有出现， 应该自行卖出或由程序隔日卖出。所以条件设置 sell_day <= 当前日
        sell_condition_2 = sell_day <= time.strftime("%Y/%m/%d",time.localtime(time.time())) \
                         and time.localtime()[3:6]>=(14,59,0) and price_updated <> True \
                         and float(quotation.result['low'][0]) <> float(dfcf_quote['topprice'])  
        
        # .3. 卖出日，非一字涨停，如果涨停价也不能触及止盈价，则已昨收盘价为基础，涨到 4% 就卖出，不用等收盘
        sell_condition_3 = sell_day <= time.strftime("%Y/%m/%d",time.localtime(time.time())) \
                         and price_updated <> True \
                         and float(dfcf_quote['topprice']) < stop_sell_price \
                         and float(quotation.result['low'][0]) <> float(dfcf_quote['topprice']) \
                         and float(quotation.result['high'][0]) >= float(quotation.result['pre_close'][0]) * 1.04 \
                         and time.localtime()[3:6]>=(9,30,0)
                                         
        #符合条件则下单卖出
        if sell_condition_0 and (sell_condition_1 or sell_condition_2 or sell_condition_3):
            #如果停牌
            if  float(quotation.result['open'][0]) == float(quotation.result['amount'][0]) ==0:
                print "\n%s %s: Suspension\n" % (quotation.result['date'][0],quotation.result['name'][0])
                while calendar.trade_time() and calendar.trade_day():
                    time.sleep(2)
            quotation.show=0
            sys.stdout.write("\r")
            sys.stdout.flush()
            log.info('Sell Begin...')
            Wtbh=trader.deal(code,dfcf_quote['name'],str(float(dfcf_quote['bottomprice'])+0.01),'S')
            if Wtbh is not None:
                log.info('Sell End...')
                #os.system("say order completed")
                #winsound.PlaySound('./wav/transaction completed.wav',winsound.SND_ASYNC)
                playsound(mac_say='transaction completed',win_sound='./wav/transaction completed.wav',frequency=450, duration=150)
                print "委托编号: [%s]\n" %  Wtbh,

                #查询当日委托状态， 如果未成则等待
                while trader.getordersdata()[-1]['Wtzt'] <> '已成':
                    sys.stdout.write("\r委托编号: [%s] 还未成交!" % Wtbh)
                    sys.stdout.flush()
                    time.sleep(5)
                sys.stdout.write("\r")
                sys.stdout.flush()
                log.info('Deal Done!')
                stock_amount=trader.getstocklist()[-1]['Kysl'] 
            else:
                break
        #每天中午12：30刷新持仓， 同时也可让Login 的 180分钟 有效期重新开始计算
        if time.localtime()[3]==12 and \
           time.localtime()[4]==30 and \
           time.localtime()[5]>10 and \
           time.localtime()[5]<12:
            show_assets()

        time.sleep(1)

def trade_time():
    print '\n\n{0:=^81}'.format('\033[20;46m TRADING TIME \033[0m')
    show_transaction()
    if quotation.kill==1:
        quotation.__init__()
    show_assets()
    stock_in_position=show_stocklist() #获取持仓的数据买卖日期

    while calendar.trade_time() and calendar.trade_day():
        if stock_in_position and int(stock_in_position['Kysl'])<>0: #如果不空仓,且有股票可卖,监视价格变化是否达到止损止盈     
            print 'Enter into Sell Porcedure...'
            monitor_sell(stock_in_position['Zqdm'],stock_in_position['buy_day'],stock_in_position['sell_day'],stock_in_position['Kysl'])
            stock_in_position=show_stocklist() #更新持仓的数据
            
        elif stock_in_position == False:  #position is empty, 需要开仓
            result= strategy.traceback()
            if result == False: #没有选出目标
                print 'Selected Stock: None! Keep Position 0\n'
                while calendar.trade_time() and calendar.trade_day():
                    if int(time.time()) % 2:
                        sys.stdout.write("\r[%s] %s" % (time.strftime("%X",time.localtime()),"--> No Trade Target !"))
                    else:
                        sys.stdout.write("\r[%s] %s" % (time.strftime("%X",time.localtime()),"-->                  "))
                    sys.stdout.flush()
                    time.sleep(1)
                    
            else: #选出目标， 开仓
                code=result["data"][0]["code"]
                codename= result["data"][0]["codeName"]
                print "%s:[%s] ---> 购买日:%s\n" %((result["stockDate"], codename,calendar.trade_calendar(result["stockDate"].replace("-","/"),2)) if result!=False else (" ","[]"," "))
                Wtbh=monitor_buy(code,codename)
                print "委托编号: [%s]\n" %  Wtbh,
                stock_in_position=show_stocklist()

        else:
            print '\n         === NO ORDERS FOR TODAY, KEEP IDLE! ==='
            quotation.stockcode=stock_in_position['Zqdm']
            quotation.show=1
            while calendar.trade_time() and calendar.trade_day():
                time.sleep(5)
        time.sleep(1)
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
    #winsound.PlaySound('./wav/good afternoon CN.wav',winsound.SND_ASYNC)
    #time.sleep(3)
    args=sys.argv
    if len(args)==5:
        strategy=Strategy(args[1],args[2],args[3],args[4])    
    else:
        strategy=Strategy("QUERY_2_DAYS_HARD",25,5,10)
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