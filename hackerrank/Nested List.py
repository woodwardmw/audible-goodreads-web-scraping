#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 15:10:33 2021

@author: mark
"""

if __name__ == '__main__':
    students = {}
    for _ in range(int(input())):
        name = input()
        score = float(input())
        students[name] = score

minScore = min(list(students.values()))
students_tmp = {key:val for key, val in students.items() if val != minScore}
secondMin = min(list(students_tmp.values()))
for i in sorted({key for key, val in students_tmp.items() if val == secondMin}):
    print(i)