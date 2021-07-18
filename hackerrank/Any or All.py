#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 12:03:37 2021

@author: mark
"""

# https://www.hackerrank.com/challenges/any-or-all/problem

n = input()
x = input().strip().split()
condition = [True,False]
for i in x:
    if(int(i) < 0):
        condition[0] = False
        break
    else:
        continue
    break
for i in x:
    j = i[::-1]
    if j == i:
        condition[1] = True
        break
    else:
        continue
    break
    
print(all(condition))


# Much simpler solution:
    
N,n = int(input()),input().split()
print(all([int(i)>0 for i in n]) and any([j == j[::-1] for j in n]))