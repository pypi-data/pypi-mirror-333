#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Logger
@author: shadow shell
"""

import os

import requests

class ShadowShell:

    def hello(self):
        print("Hello.")
    
    def request(self):
        print(requests.get("https://wwww.baidu.com"))

def testserver():
    os.system("ping shadowshell.xyz")
    
def cnnserver():
    os.system("ssh admin@shadowshell.xyz")