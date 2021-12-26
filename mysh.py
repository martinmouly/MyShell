# -*- coding: utf-8 -*-
"""
Created on Sun Dec 26 17:17:27 2021
@author: Martin
"""

def builtin(cmd):
    if cmd=='exit':
        return 0
    elif cmd=='pwd':
        return 1
    elif cmd=='cd':
        return 2
    else:
        print("error: command not found")
        
cmd=''
while cmd!='exit':
    cmd=input('mysh$ ')
    builtin(cmd)
    

