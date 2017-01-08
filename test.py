#conding=utf8

import requests
import json


s = requests.session()
res=s.post('http://www.qingdaoport.net/user/login',json.load(file("./config/account.json")));
#换成抓取的地址
r=s.get('http://www.qingdaoport.net/ywzx/zhcx/uni_cbklbcx.dw');
print r.url
#print r.text
print(r.text, '\n{}\n'.format('*'*79), r.encoding)
#r.encoding = 'GBK'
#print(r.text, '\n{}\n'.format('*'*79), r.encoding)
print r.encoding
