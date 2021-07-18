#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 14:32:09 2021

@author: mark
"""

    n = int(input())
    arr = map(int, input().split())
myList = list(arr)
first = max(myList)
print(max([i for i in myList if i != first]))