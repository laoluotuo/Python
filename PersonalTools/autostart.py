#!python3
#coding:utf-8
#该脚本功能: Windows开机后探测磁盘空置率, 若高于95%(足够空闲), 即启动测试虚拟机(会先ping探测虚拟机IP)
#然后探测虚拟磁盘G是否挂载, 若已挂载, 打开Dropbox.
import subprocess
import psutil
import os
import time


#commands
vm_ops = ['C:\\Program Files (x86)\\VMware\\VMware Workstation\\vmrun.exe', 'start', 'E:\\Virtual Machines\\CentOS7.2\\CentOS7.2.vmx']
dropbox = ['C:\\Program Files (x86)\\Dropbox\\Client\\Dropbox.exe']
keepass = ['D:\\Program Files\\Keepass\\KeePass.exe']
vm_stat = ['C:\\Program Files (x86)\\VMware\\VMware Workstation\\vmrun.exe', 'list']
disk_per = """typeperf "LogicalDisk(_Total)\% Idle Time" -sc 1""" #查询Windows计数器, 得到IO空闲率

#processes and files
process_dbx = 'dropbox.exe'
process_keepass = 'keepass.exe'
dbx_dir = 'g:\\dropbox'

def execute(command):
    """
    无输出执行命令, 无阻塞
    """
    exec_cmd = subprocess.Popen(command)
    print('Command {} excuted'.format(command))
    time.sleep(5)
    return exec_cmd

def execute_full(command):
    """
    有标准/错误输出, 可能会阻塞
    """
    exec_cmd = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return ('Command {} excuted'.format(command), exec_cmd.communicate()[0].decode('gbk'))

def proc_find(process):
    proc_lst = [ p.name().lower() for p in psutil.process_iter()]
    return True if process in proc_lst else False


def main():
    while 1:
        isdbx = proc_find(process_dbx)
        iskeepass = proc_find(process_keepass)
        isdir = os.path.exists(dbx_dir)
        isvm_run = execute_full(vm_stat)
        disk_percent = execute_full(disk_per)[1].split('"')[7]
        if float(disk_percent) > 95:
            print('>>>>>Current I/O idle percent: {}%'.format(float(disk_percent)))
            if len(isvm_run[1]) < 30:
                execute(vm_ops)
                continue
            if isdir and not iskeepass:
                execute(keepass)
                continue
            if isdir and not isdbx:
                execute(dropbox)
                continue
            elif isdir and isdbx and iskeepass:
                print('>>>>>VM is running, Disk mounted and Dropbox, Keepass is running, exit')
                time.sleep(3)
                break


if __name__ == '__main__':
    main()
