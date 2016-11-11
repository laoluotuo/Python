"""
通过su在root权限下执行命令的小工具
SSH连接用普通权限账号, 密码写在本程序中. su后会要求输入root密码
"""
#coding:UTF-8
import paramiko
import getpass
import sys

class remote():
    #在以下字段输入正确参数
    def __init__(self, ip='10.1.1.200', user='luo', password='8888888'):
        self.ip = ip
        self.user = user
        self.passwd = password
        self.conn = None
        self.ssh = None

    def con_remo(self, comm=None):
        """
        发起连接, 若不给出命令, 会示范性给出当前权限
        """
        self.ssh = ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.conn = ssh.connect(self.ip, username=self.user, password=self.passwd)
        passwd = getpass.getpass('输入您的密码, 并用双引号引用给出的命令 ')
        if comm is None:
            comm = 'echo {} | su -c {}'.format(passwd, 'whoami')
            print('当前权限是: ')
        #给出命令的情况下调用执行函数
        for i in self.exe_remo(comm, passwd):
            print(i)

    def exe_remo(self,comm, passwd, ):
        """
        执行用户命令, 并判断密码对错, 给出执行结果
        """
        std_in, std_out, std_err = self.ssh.exec_command(command='echo {} | su -c "{}"'.format(passwd, comm))
        out = std_out.readlines()
        err = std_err.readlines()
        if len(out) == 0:
            if err[0].find('Authentication failure') is not -1 :
                print('密码错误?')
            else:
                print('出现错误: ')
                err[0] = err[0].lstrip('Password: bash: ')
            yield from err
        else:
            yield from out


if __name__ == '__main__':
    client = remote()
    try:
        client.con_remo(sys.argv[1])
    except IndexError:
        client.con_remo()
