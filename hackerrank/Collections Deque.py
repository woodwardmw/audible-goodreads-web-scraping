#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 10:48:30 2021

@author: mark
"""

from collections import deque

n = int(input())
stringList = deque()
i = 1
while i <= n:
    string = str(input())
    #print(string)
    string = string.split()
    #print(string[0])
    if string[0] == 'append':
        stringList.append(string[1])
    elif string[0] == 'pop':
        stringList.pop()
    elif string[0] == 'popleft':
        stringList.popleft()
    elif string[0] == 'appendleft':
        stringList.appendleft(string[1])
      
    i += 1
    
for val in stringList:
    print(val, end = ' ')