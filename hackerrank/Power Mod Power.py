#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 16:02:39 2021

@author: mark
"""

a = (input())
b = (input())
m = (input())
if m:
    a = int(a)
    b = int(b)
    m = int(m)
else:
    a = float(a)
    b = float(b)
print(pow(a, b))
print(pow(a, b, m))