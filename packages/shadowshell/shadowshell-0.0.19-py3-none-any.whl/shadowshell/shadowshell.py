#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
from datetime import datetime

"""
ShadowShell

@author: shadow shell
"""
class ShadowShell:

    def __init__(self):
        pass

    def hello(self):
        print("Hi, i am shadow shell." )
        current_time = datetime.now()
        formatted_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        print("Now is " + formatted_current_time)

    def test(self):
        self.hello()
    
    def request(self):
        print(requests.get("https://wwww.baidu.com"))

def testserver():
    os.system("ping shadowshell.xyz")
    
def cnnserver():
    os.system("ssh admin@shadowshell.xyz")

if __name__ == "__main__":
    ShadowShell().test()