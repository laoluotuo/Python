#!/usr/bin/env python
#用于删除超大数量(rm会报参数过长)的文件.该范例是删除/tmp下tmp开头文件.
#注意修改os.chdir()中的参数为待操作路径,glob.glob内为文件查找通配符
import os
import glob

files = []
os.chdir('/tmp')
files.extend(glob.glob('tmp*'))
for f in files:
  os.remove(f)
