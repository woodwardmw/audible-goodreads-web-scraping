#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 14:22:51 2021

@author: mark
"""

    x = int(input())
    y = int(input())
    z = int(input())
    n = int(input())

print([[i, j, k] for i in range(0,x+1) for j in range(0,y+1) for k in range (0,z+1) if i + j + k != n])