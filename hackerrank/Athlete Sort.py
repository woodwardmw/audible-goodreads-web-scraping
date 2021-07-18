#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 11:38:43 2021

@author: mark
"""

#!/bin/python3

# https://www.hackerrank.com/challenges/python-sort-sort/problem

import math
import os
import random
import re
import sys



if __name__ == '__main__':
    nm = input().split()

    n = int(nm[0])

    m = int(nm[1])

    arr = []

    for _ in range(n):
        arr.append(list(map(int, input().rstrip().split())))

    k = int(input())

output = sorted(arr, key = lambda x:x[k])
for i in range(len(output)):
    print(*output[i])