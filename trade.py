#!/usr/bin/env python
# -*- coding:utf-8 -*-
#西藏同信证券股份有限公司

import sys
import requests
import json,re
import threading,Queue
import time,log
from verifycode import VerifyCode
from voice import playsound
#from winsound import Beep
#import winsound
import random,string
from PIL import Image
import cStringIO
import matplotlib.pyplot as plt

class DFCF_Trader(object):
    def __init__(self):
        self.s = requests.session()
        self.verify_code=VerifyCode()
        self.queue=Queue.Queue(maxsize=15)
        
        self.tradetime_flag=False
        self.login_flag=False
        self.kill=0

        for i in xrange(5):
            thread_queue = threading.Thread(target=self.generate_vcode_queue,name='Thread-queue-'+str(i))
            thread_queue.setDaemon(True)
            thread_queue.start()
        self.thread_login=threading.Thread(target=self.login,name='Thread-login')
        self.thread_login.setDaemon(True)
        self.thread_login.start()
 

#登陆
    def login(self):
        #log.info('%s Active...' % threading.current_thread().name)
        while True:
            if self.kill==1:
                break
            if not self.login_flag:
                #print  '[%s] : %s' % (time.strftime('%H:%M:%S') ,'Logging...')
                log.info('Logging ...')
                for i in xrange(2):
                    self.thread_auth = threading.Thread(target=self.__authorization,name='Thread-auth-'+str(i))                   
                    self.thread_auth.setDaemon(True)
                    self.thread_auth.start()
                while self.login_flag==False:
                    time.sleep(.5)
                print  '[%s] : %s' % (time.strftime('%H:%M:%S') ,'Login Success!')
                playsound(mac_say='login success',win_sound='./wav/login success.wav',frequency=450, duration=150)

            time.sleep(.5)
            
    def __authorization(self):
        while self.login_flag==False:
            headers = {'Host': 'jy.xzsec.com',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:50.0) Gecko/20100101 Firefox/50.0',
                       'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                       'Accept-Encoding':'gzip, deflate, br',
                       'Referer':'https://jy.xzsec.com/Trade/Buy',
                       'Connection':'keep-alive',
                       'Upgrade-Insecure-Requests':'1'         
                       } 
            self.s.headers.update(headers)
            login_params=json.load(file("./config/dfcf.json"))
    
            #获取验证码：
            try:
                randNum,vcode=self.queue.get(block=False)
                print "use queue: %d, vcode: %s, randNum: %s" % (self.queue.qsize(),vcode,randNum)
            except:
                randNum="%.16f" % float(random.random())
                url_yzm="https://jy.xzsec.com/Login/YZM?randNum=" + randNum
                #img = Image.open(cStringIO.StringIO(self.s.get(url_yzm).content))
                #img.show()
                #vcode=raw_input('Enter:')
                vcode=""; digits=list(string.digits); i=0
                while True:
                    if self.login_flag==True: return
                    vcode,im=self.verify_code.get_verify_code(url_yzm)
                    if len(vcode) == 4:                        
                        for k in xrange(4):
                            if vcode[k] not in digits: #[str(x) for x in xrange(10)]:
                                break
                        else:
                            #plt.figure("verify code")
                            #plt.imshow(im)
                            #plt.show()
                            print  "\rCode:[%4s]    Retry Times:%2d" % (vcode, i)
                            break
                    sys.stdout.write(u"\r验证码识别:%s " % (vcode))
                    sys.stdout.flush()
                    i+=1
            
            if self.login_flag==True: return

            login_params.update({'identifyCode':vcode,'randNumber':randNum})            
            res=self.s.post('https://jy.xzsec.com/Login/Authentication',login_params)
            
            if int(res.json()["Status"]) <> 0:
                playsound(mac_say='login failed',win_sound='./wav/login failed.wav',frequency=450, duration=150)
                continue
 
            if self.login_flag==True: return
            
            #获取 validatekey：
            get_validatekey=self.s.get('https://jy.xzsec.com/Trade/Buy')
            if re.search(r'em_validatekey.*?>',get_validatekey.text).group():
                self.validatekey= re.search(r'em_validatekey.*?>',get_validatekey.text).group()[37:73]
                #print "\nvalidatekey: %s" % self.validatekey
                self.url_suffix='?validatekey='+self.validatekey
                
                self.login_flag=True        
                self.login_message=res.json()
                return self.login_message
            else:
                continue



#登陆
    def login_a(self):
        #log.info('%s Active...' % threading.current_thread().name)
        while True:
            if self.kill==1:
                break
            if not self.login_flag:
                #print  '[%s] : %s' % (time.strftime('%H:%M:%S') ,'Logging...')
                log.info('Logging ...')
                try:
                    self.__authorization()
                    #print  '[%s] : %s' % (time.strftime('%H:%M:%S') ,'Login Success!')
                    if self.login_flag==True:
                        log.info('Login Success')
                        #os.system("say login success")
                        #Beep(450,150)
                        #winsound.PlaySound('./wav/login success.wav',winsound.SND_ASYNC)
                        playsound(mac_say='login success',win_sound='./wav/login success.wav',frequency=450, duration=150)
                    else:
                        log.info('Login Failed')
                        #Beep(450,150)
                        playsound(mac_say='login failed',win_sound='./wav/login failed.wav',frequency=450, duration=150)
                        time.sleep(3)                    
                except Exception:
                    #winsound.PlaySound('./wav/connection lost.wav',winsound.SND_ASYNC)
                    #os.system("say connection lost")
                    #Beep(600,500)
                    playsound(mac_say='connection lost',win_sound='./wav/connection lost.wav',frequency=600, duration=500)
                    time.sleep(1)
                    log.info("Login connection lost !!!")
            time.sleep(.5)
            
    def __authorization_a(self):
        headers = {'Host': 'jy.xzsec.com',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:50.0) Gecko/20100101 Firefox/50.0',
                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                   'Accept-Encoding':'gzip, deflate, br',
                   'Referer':'https://jy.xzsec.com/Trade/Buy',
                   'Connection':'keep-alive',
                   'Upgrade-Insecure-Requests':'1'         
                   } 
        self.s.headers.update(headers)
        login_params=json.load(file("./config/dfcf.json"))

        #获取验证码：
        try:
            randNum,vcode=self.queue.get(block=False)
            print "use queue: %d, vcode: %s, randNum: %s" % (self.queue.qsize(),vcode,randNum)
        except:
            randNum="%.16f" % float(random.random())
            url_yzm="https://jy.xzsec.com/Login/YZM?randNum=" + randNum
            #img = Image.open(cStringIO.StringIO(self.s.get(url_yzm).content))
            #img.show()
            #vcode=raw_input('Enter:')
            vcode=""; digits=list(string.digits); i=0
            while True:
                vcode,im=self.verify_code.get_verify_code(url_yzm)
                if len(vcode) == 4:                        
                    for k in xrange(4):
                        if vcode[k] not in digits: #[str(x) for x in xrange(10)]:
                            break
                    else:
                        #plt.figure("verify code")
                        #plt.imshow(im)
                        #plt.show()
                        print  "\rCode:[%4s]    Retry Times:%2d" % (vcode, i)
                        break
                sys.stdout.write(u"\r验证码识别:%s " % (vcode))
                sys.stdout.flush()
                i+=1

        login_params.update({'identifyCode':vcode,'randNumber':randNum})            
        res=self.s.post('https://jy.xzsec.com/Login/Authentication',login_params)
        
        if int(res.json()["Status"]) <> 0:
            return
        
        #获取 validatekey：
        get_validatekey=self.s.get('https://jy.xzsec.com/Trade/Buy')
        if re.search(r'em_validatekey.*?>',get_validatekey.text).group():
            self.validatekey= re.search(r'em_validatekey.*?>',get_validatekey.text).group()[37:73]
            #print "\nvalidatekey: %s" % self.validatekey
            self.url_suffix='?validatekey='+self.validatekey
            
            self.login_flag=True        
            self.login_message=res.json()
            return self.login_message
        else:
            return
        '''
        self.login_message= "message(%s), Status(%s)" % (res.json()["Message"], res.json()["Status"])
        for i in xrange(len(res.json()["Data"])):
            for key  in res.json()["Data"][i]:
                    self.login_message += key +" %s" % res.json()["Data"][i][key]
        '''        
        

#生成验证码队列
    def generate_vcode_queue(self):
        while True:
            if self.kill==1:
                break
            randNum="%.16f" % float(random.random())
            url_yzm="https://jy.xzsec.com/Login/YZM?randNum=" + randNum
            vcode=""; digits=list(string.digits)
            while True:
                vcode,im=self.verify_code.get_verify_code(url_yzm)
                if len(vcode) == 4:                        
                    for k in xrange(4):
                        if vcode[k] not in digits: #[str(x) for x in xrange(10)]:
                            break
                    else:
                        #print  "qsize: %2d" % self.queue.qsize()
                        break
            self.queue.put([randNum, vcode],block=True)
            #time.sleep(.5)

        
#资产列表
    def getassets(self):
        while True:
            try:
                Assets=self.s.post('https://jy.xzsec.com/Com/GetAssets'+self.url_suffix,
                                   {'moneyType':'RMB'},timeout=5)
            except Exception:
                print "\n<getassets> Connection Lost, Re-Connecting..."
                time.sleep(1)
            else:
                try:
                    return Assets.json()["Data"][0]                    
                except ValueError:
                    self.login_flag=False
                    while self.login_flag is False:
                        time.sleep(.5)
                except TypeError: #Status:-1; Message:'服务器异常'
                    print u"\n <getassets> 服务器异常!"
                    time.sleep(2)
                except Exception as e:
                    log.error(e)
                    time.sleep(2)
                    
                '''                
                if Assets.json()["Status"]!=0: #Status:-2 ; Message:"会话已超时，请重新登录!"
                    self.login_flag=False
                    time.sleep(2)
                    continue
                return Assets.json()["Data"][0]
                '''

#持仓列表
    def getstocklist(self):
        while True:
            try:
                StockList=self.s.post('https://jy.xzsec.com/Search/GetStockList'+self.url_suffix,
                                      {'qqhs':'1000','dwc':''});
            except Exception:
                print "\n <getstocklist> connection lost!"
                time.sleep(1)
            else:
                try:
                    return StockList.json()["Data"]                    
                except ValueError:
                    self.login_flag=False
                    while self.login_flag is False:
                        time.sleep(.5)
                except Exception as e:
                    log.error(e)
                    time.sleep(2) 
                     
            '''    
            self.stocklist_message=""
            StockList=self.s.post('https://jy.xzsec.com/Search/GetStockList',{'qqhs':'1000','dwc':''});
            if len(StockList.json()["Data"])==0:
                print "Stock Position:  0"
            else:
                for i in xrange(len(StockList.json()["Data"])):
                    for key  in StockList.json()["Data"][i]:
                        self.stocklist_message += key +":%s  " % StockList.json()["Data"][i][key]
           '''
#当日委托
    def getordersdata(self):
        while True:
            try:
                OrdersData=self.s.post('https://jy.xzsec.com/Search/GetOrdersData'+self.url_suffix,{'qqhs':'20','dwc':''});
            except Exception:
                print "\n <getordersdata> connection lost!"
                time.sleep(1)
            else:
                try:
                    return OrdersData.json()["Data"]
                except ValueError:
                    self.login_flag=False
                    while self.login_flag is False:
                        time.sleep(.5)
                except Exception as e:
                    log.error(e)
                    time.sleep(2)
        '''            
        self.ordersdata_message=""
        OrdersData=self.s.post('https://jy.xzsec.com/Search/GetOrdersData'+self.url_suffix,{'qqhs':'20','dwc':''});
        if len(OrdersData.json()["Data"])==0:
            print "Orders:  0"
        else:
            for i in xrange(len(OrdersData.json()["Data"])):
                for key  in OrdersData.json()["Data"][i]:
                    self.ordersdata_message += key +":%s \n" % OrdersData.json()["Data"][i][key]
        '''
#当日成交
    def gettodaydealdata(self):
        while True:
            try:
                TodayDealData=self.s.post('https://jy.xzsec.com/Search/GetDealData'+self.url_suffix,{'qqhs':'20','dwc':''});
            except Exception:
                print "\n <gettodaydealdata> connection lost!"
                time.sleep(1)
            else:
                try:
                    return TodayDealData.json()["Data"]                    
                except ValueError:
                    self.login_flag=False
                    while self.login_flag is False:
                        time.sleep(.5)         
                except Exception as e:
                    log.error(e)
                    time.sleep(2)         

#历史成交
    def gethisdealdata(self,st='2017-02-01',et='2017-02-12'):
        while True:
            try:
                HistDealList=self.s.post('https://jy.xzsec.com/Search/GetHisDealData'+self.url_suffix, \
                                      {'st':st,'et':et,'qqhs':'1000','dwc':''});
            except Exception:
                print "\n <getstocklist> connection lost!"
                time.sleep(1)
            else:
                try:
                    return HistDealList.json()["Data"]                    
                except ValueError:
                    self.login_flag=False
                    while self.login_flag is False:
                        time.sleep(.5)
                except Exception as e:
                    log.error(e)
                    time.sleep(2) 
       
#撤单列表
    def getrevokelist(self):
        try:
            RevokeList=self.s.post('https://jy.xzsec.com/Trade/GetRevokeList'+self.url_suffix,timeout=3)
        except Exception:
            self.login_flag=False
        list=[]
        if len(RevokeList.json()["Data"])==0:
            print "Revoke List: %2d" % (0)
        else:           
            for i in xrange(len(RevokeList.json()["Data"])):
                list.append(RevokeList.json()["Data"][i]["Wtrq"]+"_"+ \
                            RevokeList.json()["Data"][i]["Wtbh"])                    
        return list

#撤单
    def revoke(self,wtbh):    
        RevokeOrders=self.s.post('https://jy.xzsec.com/Trade/RevokeOrders'+self.url_suffix,{'revokes':wtbh})
        return RevokeOrders

#下单
    def deal(self,stockcode,stockname,price,fen_cang,tradetype):
        while True:
            try:
                GetKyzjAndKml=self.s.post('https://jy.xzsec.com/Trade/GetKyzjAndKml'+self.url_suffix, \
                                     {'stockCode':stockcode,'zqmc':stockname,'price':price,'tradeType':tradetype});
                #Kmml=GetKyzjAndKml.json()["Data"]["Kmml"]
                Kyzj=GetKyzjAndKml.json()["Data"]["Kyzj"]
                Kmml=str(int(float(Kyzj)/float(price)/100/fen_cang))
                #print GetKyzjAndKml.json()
                if Kmml=='0':
                    print u'可交易数量为0'
                    time.sleep(5)
                    break
            except ValueError: # ValueError: No JSON object could be decoded 超时返回登录前网页
                self.login_flag=False
                while self.login_flag is False:
                    time.sleep(.5)
                continue
            except Exception as e:
                print e,"\n<GetKyzjAndKml> Connection Lost, Re-Connecting..."
                time.sleep(1)
                continue
        
            try:
                SubmitTrade=self.s.post('https://jy.xzsec.com/Trade/SubmitTrade'+self.url_suffix, \
                                   {'stockCode':stockcode,'price':price, \
                                   'amount':Kmml, \
                                   'tradeType':tradetype} #,'stockName':stockname
                                   )       
            except Exception as e:
                print e,"\n<SubmitTrade> Connection Lost, Re-Connecting..."
                time.sleep(1)
            else:
                try:
                    #print GetKyzjAndKml.json()
                    #print SubmitTrade.json()    
                    Wtbh=SubmitTrade.json()["Data"][0]["Wtbh"]
                    return Wtbh
                except ValueError: 
                    self.login_flag=False
                    while self.login_flag is False:
                        time.sleep(.5)
                    continue
                except (IndexError,TypeError):
                    log.error(SubmitTrade.json()["Message"]) #Status:-1
                    break               
                except Exception as e:
                    print e,'unknow error!'
                    time.sleep(2)
                
#获取实时行情
    def getquote(self,stockcode):
        params={
                'id':stockcode,
                'callback':'',#'jQuery18302588442438663068_1484803703313',
                '_':'' # repr(time.time()).replace(".","")
               }
        while True:
            try:
                quote=self.s.get('https://hsmarket.eastmoney.com/api/SHSZQuoteSnapshot',params = params)
                break
            except Exception as e:
                print e;time.sleep(1)
                continue
        return eval(re.search(r'{.*}',quote.text).group())
        

