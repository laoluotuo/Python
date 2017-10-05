#!/usr/bin/env python
#coding=utf-8
#功能:删除指定目录下超过指定时间(默认1个月)的.log文件,且对超过500M的大文件做报警
#注:脚本执行后,会把日志输出到/tmp/log_cleaner.log中
#   若同类log文件少于5个,会跳过而不删除.可在cleaner函数中修改该参数

import os
import logging
import time
import argparse



def file_scanner(path, path_except, ext_name='.log', time_range=2592000): #文件扫描器, 返回格式为(目录名, 文件列表)的字典
    os.chdir(path)
    file_objects = dict()
    bigfiles = []
    current_time = time.time()
    try:
        for root, dirs, files in os.walk(path):
            file_list = []
            for dir in path_except:
                rt, sub = os.path.split(dir)    #拆分排除路径, 比较当前迭代器中是否有它
                if  rt == root and sub in dirs:
                    dirs.remove(sub)
            for file in files:
                file_path = os.path.join(root, file)
                if root.startswith(path_except) or os.path.islink(file_path):
                    continue
                elif file.endswith(ext_name) and current_time - os.stat(file_path).st_mtime > time_range:
                    file_list.append(file_path)
                size = os.stat(file_path).st_size
                if size > 524288000 :
                    bigfiles.append(file_path)
            if file_list:
                file_objects[root] = file_list
    except Exception as e:
        logging.warning(e)
    return (file_objects, bigfiles)


def file_sorter(files): #文件分类器, 对单一目录下的文件按文件名头分类, 返回格式为(文件头:文件列表)格式字典
    sorted_files = dict()
    file_types = set()
    for f in files:
        file_types.add(os.path.split(f)[1][:3]) #取出文件名的头三位字符用于文件分类
    for f_type in file_types:
        sorted_files[f_type] = [] #每类文件添加一个空列表
    for f in files:
        sorted_files[os.path.split(f)[1][:3]].append(f)
    return sorted_files


def cleaner(folder, files, file_keep=5): #文件清理器, 按文件最后写时间删除文件. 默认保留最近一个月的
    if len(files) < file_keep:
        logging.info('目录%s 下类似于 %s 的文件少于%s个,久未更新或非每日日志?已略过' % (folder, files[0], file_keep))
    else:
        for f in sorted(files):
            os.remove(f)
            logging.warning('已删除文件: %s' % f)


def main(path, path_except, time_range=2592000): #执行删除操作,并屏幕输出日志,默认时间范围time_range为大于一个月(2592000秒)
    if not os.path.exists(path):
        logging.warning('路径 %s 不存在,跳过...' % path)
        return 
    logging.warning('>>>开始删除 %s 下过期文件...' % path)

    scan_res = file_scanner(path, path_except=path_except, time_range=time_range)
    for folder, files in scan_res[0].items():
        for _, sub_files in file_sorter(files).items():
            cleaner(folder, sub_files)
    logging.warning('删除操作完成.')
    for file in scan_res[1]:
        logging.warning('发现超大文件: %s, 大小: %sMB  需手动处理' % (file, os.stat(file).st_size / 1048576))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='本脚本用于删除指定目录下超过指定时间(默认1个月)的.log文件,且对超过500M的大文件做报警')
    parser.add_argument('-e',  action='store', help='要排除的路径', type=str, default='0')
    parser.add_argument('-f',  action='store', help='排除路径的配置文件', type=str, default='except_paths.txt')
    parser.add_argument('-v',  action='store_true', help='显示log信息,而非存储到文件')
    args = parser.parse_args()
    except_path = args.e
    except_file = args.f
    verbose = args.v

    #以下为预定义变量
    paths = [
        '/data',
        '/opt',
        '/var',
        '/usr/local'
    ]
    path_except = ('/proc', '/sys', '/dev')
    log_name = '/tmp/log_cleaner.log'


    if verbose:                     #日志控制台显示或写入文件
        logging.basicConfig(
            level = logging.WARNING,
            format = '%(asctime)s : %(levelname)s : %(message)s',
        )
    else:
        logging.basicConfig(
            level = logging.WARNING,
            format = '%(asctime)s : %(levelname)s : %(message)s',
            filename = log_name,
            filemode = 'w'
        )

    if except_path != '0':          #添加排除路径
        path_except += (except_path, )
        if except_path in paths:
            paths.remove(except_path)

    except_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), except_file)
    if os.path.exists(except_file): #路径排除文件处理
        content = open(except_file, 'r').readlines()
        if content:
            path_except += tuple([line.strip() for line in content])
            for ex in [line.strip() for line in content]:
                if ex in paths:
                    paths.remove(ex)
    # logging.warning('当前except_path: %s' % ' '.join(path_except))

    for path in paths:              #执行日志清理主函数
        main(path, path_except, time_range=2592000)
    logging.warning('清理完成.')
