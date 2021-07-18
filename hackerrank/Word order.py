#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 09:14:42 2021

@author: mark
"""

n = int(input())
stringList = []
i = 1
while i <= n:
    stringList.append(str(input()))
    i += 1
    
outputDict = {}
for string in stringList:
    if string in outputDict:
        outputDict[string] += 1
    else:
        outputDict[string] = 1
        
print(len(outputDict))
for i in outputDict.values():
    print (i, end = ' ')