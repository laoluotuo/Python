# coding:UTF-8
import os
def listdirs(path=None):
    """
    广度优先搜索 . 属于"先序遍历"
    函数将接收一个路径参数,默认为'.'
    之后循环中用os.listdir()函数将路径取出最后的部分,可能是子目录/文件
    是目录的,继续放入dirs,继续循环拆分,直到为空
    是文件的,放入files,是合并了path的完整带路径文件
    """
    if path is None:
        path = '.'
    dirs = [path]
    files = []
    while dirs:
        path = dirs.pop()
        for f in os.listdir(path):
            f = os.path.join(path, f)
            #下面判断迭代出的对象是文件还是目录.注意要用完整路径,为了能迭代子目录.
            if os.path.isdir(f):
                dirs.append(f)
                print(dirs)
            else:
                files.append(f)
    return files, len(files)

def deep_listdirs(path=None):
    """
    深度优先搜索,编写了函数deep_search,用于递归.属于"中序遍历"
    与广度优先不同的是,dirs里只要有目录,就纵深查找,直到里面无目录了,才做files.append操作.
    """
    if path is None:
        path = '.'
    dirs = [path]
    files = []
    def deep():
        path = dirs.pop()
        for i in os.listdir(path):
            i = os.path.join(path, i)
            if os.path.isdir(i):
                dirs.append(i)
                print(dirs)
                deep()
            else:
                files.append(i)
    deep()
    return files, len(files)



print(deep_listdirs('D:\\Program Files\\Mozilla Firefox'))
# print(listdirs('D:\\Program Files\\Mozilla Firefox'))
