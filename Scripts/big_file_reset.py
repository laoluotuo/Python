#!/usr/bin/env python
#coding=utf-8
#大文件缩减程序.默认清理超过500M的.out文件,缩减到200M
import argparse
import logging
import tempfile
import os



logging.basicConfig(
    level = logging.WARNING,
    format = '%(asctime)s : %(levelname)s : %(message)s',
)
path_except = ('/proc', '/sys', '/dev')


def file_scanner(path, ext_name='.out', path_except=path_except): #文件扫描器, 返回格式为(目录名, 文件列表)的字典
    os.chdir(path)
    bigfiles = []
    try:
        for root, dirs, files in os.walk('.'):
            root_abs = os.path.abspath(root)
            for file in files:
                file_path = os.path.join(root_abs, file)
                size = os.stat(file_path).st_size
                if os.path.islink(file_path) or root_abs.startswith(path_except):
                    continue
                elif file.endswith(ext_name) and size > 524288000:
                    bigfiles.append(file_path)
    except Exception as e:
        logging.warning(e)
    if bigfiles:
        for f in bigfiles:
            logging.warning('发现大文件: %s, 大小: %sM' % (f, os.stat(f).st_size / 1048576))
    else:
        logging.warning('未发现大文件')
    return bigfiles


def file_cutter(big_file):
    temp_f = tempfile.NamedTemporaryFile(delete=True)
    logging.warning('>>>开始消减 %s' % big_file)

    with open(big_file, 'r+') as f:
        try:
            f.seek(-204800000, 2)
        except IOError:
            logging.warning('IOError..文件大小低于200M? 脚本退出')
            return
        for line in f:
            temp_f.write(line)
    #logging.warning(temp_f.name + ' 大小: %s' % os.stat(temp_f.name).st_size)
    with open(big_file, 'w') as f:
        with open(temp_f.name, 'r') as t:
            for line in t:
                f.write(line)
    logging.warning('文件已削减,当前大小: %sM' % (os.stat(big_file).st_size / 1048576))
    temp_f.close()


def main(path, ext_name='.out', path_except=path_except):
    if not os.path.exists(path):
        logging.warning('路径 %s 不存在,跳过...' % path)
        return
    logging.warning('>>>正在搜索 %s 下超大文件...' % path)
    scan_res = file_scanner(path,  ext_name, path_except)
    for big_file in scan_res:
        file_cutter(big_file)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='本脚本用于遍历并削减特定扩展名的大文件')
    parser.add_argument('-e',  action='store', help='需削减文件的扩展名', type=str, default='.out')
    args = parser.parse_args()
    ext_name = args.e

    paths = [
        '/data',
        '/opt',
        '/var',
        '/home',
        '/usr/local'
    ]
    for path in paths:
        main(path, ext_name)
    logging.warning('大文件削减完成.')
