#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 19:07:54 2021

@author: mark
"""
#https://www.hackerrank.com/challenges/ginorts/problem

string = input()
lower = [i for i in string if i.islower()]
lower.sort()
upper = [i for i in string if i.isupper()]
upper.sort()
odd = [i for i in string if i.isnumeric() and int(i) % 2 == 1]
odd.sort()
even = [i for i in string if i.isnumeric() and int(i) % 2 == 0]
even.sort()
output = lower + upper + odd + even
print(*output, sep = '')