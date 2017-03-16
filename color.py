#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 显示格式: \033[显示方式;前景色;背景色m  
# ------------------------------------------------  
# 显示方式             说明  
#   0                 终端默认设置  
#   1                 高亮显示  
#   4                 使用下划线  
#   5                 闪烁  
#   7                 反白显示  
#   8                 不可见  
#   22                非粗体  
#   24                非下划线  
#   25                非闪烁  
#  
#   前景色             背景色            颜色  
#     30                40              黑色  
#     31                41              红色  
#     32                42              绿色  
#     33                43              黃色  
#     34                44              蓝色  
#     35                45              紫红色  
#     36                46              青蓝色  
#     37                47              白色  
# ------------------------------------------------  
# -----------------colorama模块的一些常量---------------------------  
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.  
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.  
# Style: DIM, NORMAL, BRIGHT, RESET_ALL  
#  
  
try:
    from colorama import  init, Fore, Back, Style  
except ImportError:
    class Colored(object):  
        # 显示格式: \033[显示方式;前景色;背景色m  
        # 只写一个字段表示前景色,背景色默认  
        RED = '\033[31m'       # 红色  
        GREEN = '\033[32m'     # 绿色  
        YELLOW = '\033[33m'    # 黄色  
        BLUE = '\033[34m'      # 蓝色  
        FUCHSIA = '\033[35m'   # 紫红色  
        CYAN = '\033[36m'      # 青蓝色  
        WHITE = '\033[37m'     # 白色      
        #: no color  
        RESET = '\033[0m'      # 终端默认颜色  
      
        def color_str(self, color, s):  
            return '{}{}{}'.format(  
                getattr(self, color),  
                s,  
                self.RESET  
            )  
      
        def red(self, s):  
            return self.color_str('RED', s)  
      
        def green(self, s):  
            return self.color_str('GREEN', s)  
      
        def yellow(self, s):  
            return self.color_str('YELLOW', s)  
      
        def blue(self, s):  
            return self.color_str('BLUE', s)  
      
        def fuchsia(self, s):  
            return self.color_str('FUCHSIA', s)  
      
        def cyan(self, s):  
            return self.color_str('CYAN', s)  
      
        def white(self, s):  
            return self.color_str('WHITE', s)     
    color = Colored()
else:
    init(autoreset=True)  
    class Colored(object):        
        #  前景色:红色  背景色:默认  
        def red(self, s):  
            return Fore.RED + s + Fore.RESET       
        #  前景色:绿色  背景色:默认  
        def green(self, s):  
            return Fore.GREEN + s + Fore.RESET      
        #  前景色:黄色  背景色:默认  
        def yellow(self, s):  
            return Fore.YELLOW + s + Fore.RESET    
        #  前景色:蓝色  背景色:默认  
        def blue(self, s):  
            return Fore.BLUE + s + Fore.RESET       
        #  前景色:洋红色  背景色:默认  
        def magenta(self, s):  
            return Fore.MAGENTA + s + Fore.RESET      
        #  前景色:青色  背景色:默认  
        def cyan(self, s):  
            return Fore.CYAN + s + Fore.RESET       
        #  前景色:白色  背景色:默认  
        def white(self, s):  
            return Fore.WHITE + s + Fore.RESET       
        #  前景色:黑色  背景色:默认  
        def black(self, s):  
            return Fore.BLACK     
        #  前景色:白色  背景色:绿色  
        def white_green(self, s):  
            return Fore.LIGHTWHITE_EX +  Back.GREEN + s + Fore.RESET + Back.RESET    
        #  前景色:白色  背景色:红色  
        def white_red(self, s):  
            return Fore.LIGHTWHITE_EX +  Back.RED + s   
        #  前景色:白色  背景色:青色  
        def white_cyan(self, s):  
            return Fore.LIGHTWHITE_EX +  Back.CYAN  + s 
        #  前景色:白色  背景色:红色  
        def white_magenta(self, s):  
            return Fore.LIGHTWHITE_EX +  Back.MAGENTA + s      
         #  前景色:白色  背景色:蓝色  
        def white_blue(self, s):  
            return Fore.LIGHTWHITE_EX +  Back.BLUE  + s   
        #  前景色:白色  背景色:黄色  
        def white_yellow(self, s):  
            return Fore.LIGHTWHITE_EX +  Back.YELLOW + s      
    color = Colored()
    
'''
print color.red('I am red!')  
print color.green('I am gree!')  
print color.yellow('I am yellow!')  
print color.blue('I am blue!')  
print color.magenta('I am magenta!')  
print color.cyan('I am cyan!')  
print color.white('I am white!')  
print color.white_green('I am white green!')
print color.white_red('I am white green!')
print color.white_cyan('I am white green!')
print color.white_magenta('I am white green!')
print color.white_blue('I am white green!')
print color.white_yellow('I am white green!') 
print(Style.DIM + 'and in dim text')
'''