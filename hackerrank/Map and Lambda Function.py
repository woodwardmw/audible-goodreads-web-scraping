#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 19:28:53 2021

@author: mark
"""

# https://www.hackerrank.com/challenges/map-and-lambda-expression/problem

cube = lambda x: x ** 3

def fibonacci(n):
    fib = []
    if n > 0:
        fib = [0]
    if n > 1:
        fib = [0,1]
    if n > 2:
        for i in range(2,n):
            fib.append(fib[i-1] + fib[i-2])  # return a list of fibonacci numbers
            i+=1
    return fib
    

if __name__ == '__main__':
    n = int(input())
    print(list(map(cube, fibonacci(n))))