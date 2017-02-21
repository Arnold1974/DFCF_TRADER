#!/usr/bin/env python
#-*- coding:utf-8 -*-

try:
    import pytesseract
    from PIL import Image
except ImportError:
    print '模块导入错误,请使用pip安装,pytesseract依赖以下库：'
    print 'http://www.lfd.uci.edu/~gohlke/pythonlibs/#pil'
    print 'http://code.google.com/p/tesseract-ocr/'
    raise SystemExit

#将图片放到内存中
import cStringIO, urllib2
import matplotlib.pyplot as plt
import sys
url_dfcf="https://jy.xzsec.com/Login/YZM?randNum=0.5609794557094574"

class VerifyCode(object):
    def get_verify_code(self):
        #url ="http://www.qqct.com.cn/console/captcha"
        
        file = urllib2.urlopen(url_dfcf)
        tmpIm = cStringIO.StringIO(file.read())
        im = Image.open(tmpIm)
        '''
        im_1=im.crop((10,0,85,35)) #crop() : 从图像中提取出某个矩形大小的图像。它接收一个四元素的元组作为参数，
                            #各元素为（left, upper, right, lower），坐标系统的原点（0, 0）是左上角。
        imgry = im.convert('L')
        #imgry.show()
        threshold = 190  
        table = []  
        for i in range(256):  
            if i < threshold:  
                table.append(0)  
            else:  
                table.append(1) 
        out = imgry.point(table,'1')        
        #print im.format, im.size, im.mode
        #im.show()
        '''
        vcode = pytesseract.image_to_string(image=im, lang="eng", config="-psm 7")
      
        #对于识别成字母的 采用该表进行修正  
        rep={'O':'0',  
            'I':'1','L':'1',  
            'Z':'2',  
            'S':'8',
            ' ':''
            };  
        for r in rep:  
            vcode = vcode.replace(r,rep[r]) 
        return vcode,im

if __name__=="__main__":
    test=VerifyCode()
    i=0;vcode=""
    while len(vcode)<>10 and i<1000:
        vcode,im=test.get_verify_code()     
        if len(vcode)==4:
            for k in xrange(4):
                if vcode[k] not in [str(x) for x in xrange(10)]:
                    break
            else:
                plt.figure("verify code")
                plt.imshow(im)
                plt.show()
                print  "\rCode:[%4s]    Length:%2d" % (vcode, len(vcode))
        sys.stdout.write( "\rCode:[%8s]    Length:%2d   Count: %d" % (vcode, len(vcode),i))
        i+=1
    print '\nDone'