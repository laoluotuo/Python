# coding:UTF-8
import os
def walk_1(root):
    stack = [root]
    files = []
    while stack:
        cur = stack.pop()           #用栈模式,是深度优先搜索,形式为后序遍历
        for x in os.scandir(cur):
            if x.is_dir():
                stack.append(x.path)
            else:
                files.append(x.path)
    return files

def walk_2(root):
    queue = [root]
    files = []
    while queue:
        cur = queue.pop(0)          #用队列模式,是广度优先搜索,形式为先序遍历
        for x in os.scandir(cur):
            if x.is_dir():
                queue.append(x.path)
            else:
                files.append(x.path)
    return files

def walk_1(root):
    files = []
    for x in os.scandir(root):
        if x.is_dir():
            yield from walk_1(x.path)
        else:
            yield x.path

print(walk_1('D:\\Program Files\\Mozilla Firefox'))
