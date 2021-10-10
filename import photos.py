#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 19:44:13 2021

@author: mark
"""
from os import listdir
import re
from shutil import copyfile
# from icecream import ic

externalLocation = '/media/mark/disk/DCIM/100MSDCF'
internalLocation = '/home/mark/Processing'
internalContents = listdir(internalLocation)
externalContents = listdir(externalLocation)

# ic(sorted(internalContents))
p = re.compile(r'DSC(\d\d\d\d\d)\.ARW$')
internalFiles = [s for s in internalContents if p.match(s)]
lastInternalFile = sorted(internalFiles)[-1]
externalFiles = [s for s in externalContents if p.match(s)]
lastExternalFile = sorted(externalFiles)[-1]
lastInternalCount = int(p.match(lastInternalFile)[1])
lastExternalCount = int(p.match(lastExternalFile)[1])

count = int(lastInternalCount) + 1

while count <= lastExternalCount:
    src = externalLocation + '/DSC' + f'{count:05d}' + '.ARW'
    dst = internalLocation + '/DSC' + f'{count:05d}' + '.ARW'
    try:
        copyfile(src, dst)
        print(src,dst)
    except FileNotFoundError:
        ic(src + " does not exist")
    src = externalLocation + '/DSC' + f'{count:05d}' + '.JPG'
    dst = internalLocation + '/jpeg/DSC' + f'{count:05d}' + '.JPG'
    try:
        copyfile(src, dst)
        print(src,dst)
    except FileNotFoundError:
        ic(src + " does not exist")
    count += 1
