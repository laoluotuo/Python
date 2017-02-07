#!python 3.5
#coding:utf-8
#该脚本功能是, 开机启动测试虚拟机(vm_ops), 然后探测虚拟磁盘G是否挂载, 挂载后打开Dropbox.
import subprocess
import psutil
import os
import time

#commands
vm_ops = ['C:\\Program Files (x86)\\VMware\\VMware Workstation\\vmrun.exe', 'start', 'E:\\Virtual Machines\\CentOS7.2\\CentOS7.2.vmx']
dbx_start = ['C:\\Program Files (x86)\\Dropbox\\Client\\Dropbox.exe']
vm_ping = ['ping', '-n', '1', '-w', '800', '192.168.116.128']

#processes and files
process_dbx = 'dropbox.exe'
dbx_dir = 'g:\\dropbox'

def execute(command):
    exec_cmd = subprocess.Popen(command)
    return exec_cmd

def ping(vm_ping):
    try:
        output = subprocess.check_output(vm_ping)
        print(output)
        return 0
    except Exception as e:
        print(e)
        return 1

def proc_find(process):
    proc_lst = [ p.name().lower() for p in psutil.process_iter()]
    return True if process in proc_lst else False

def exists(obj):
    return os.path.exists(obj)

def main():
    time.sleep(0)
    execute(vm_ops)
    while 1:
        isdbx = proc_find(process_dbx)
        isdir = exists(dbx_dir)
        if isdir and not isdbx:
            execute(dbx_start)
            break
        elif isdir and isdbx:
            break
        time.sleep(3)
if __name__ == '__main__':
    main()
