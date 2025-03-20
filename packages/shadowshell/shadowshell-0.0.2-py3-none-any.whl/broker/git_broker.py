#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitBroker

@author: shadow shell
"""

import os

class GitBroker:
    
    def acp(self):
        os.system("git add -A && git commit -m 'UPDATE: update somethings.' && git push")
            
    def view_config(self):
        os.system("git config user.name & git config user.email")

