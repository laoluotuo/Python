#coding:UTF-8
import os
import paramiko
import sys

class scp:
    """
    放在init中的是初始化好后就不会丢失的东西, 而函数中如conn, 连接后做完事情就自动退出, 关闭连接了.
    """
    def __init__(self, host='10.1.1.2', username='root', password='MYPASSWORD', path='/root/study/'):
        self.host = host
        self.username = username
        self.password = password
        self.path = path
        self.ssh = None
        self.sftp = None


    def conn(self):
        """
        连接SSH服务器 
        """
        self.ssh = conssh = paramiko.SSHClient() #连接赋值给self.ssh,防止无引用连接丢失(或被回收)
        conssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conssh.connect(self.host, username=self.username,password=self.password )
        self.sftp = conssh.open_sftp() #连接赋值给self.sftp, 防止无引用连接丢失(或被回收)


    def getmode(self, file):
        """
        取得远程文件权限 
        """
        std_in, std_out, std_err = self.ssh.exec_command('stat %s |grep -E -o "\([0-7]{4}"'% file) #正则表达式用format()报错, 改用print
        return int(std_out.readlines()[0].strip()[-3:])


    def puts(self, src, dest=None):
        """
        上传文件
        注意:sftp.put会覆盖原文件不提示, sftp.stat测试文件, 若存在无报错, 不存在报错且中断程序.
        """
        if dest is None:
            dest = self.path
        #末尾自动添加/, 防止路径格式错误
        if not dest.endswith('/'):
            dest = dest + '/'

        std_in, std_out, std_error = self.ssh.exec_command('cd {} && pwd'.format(dest))
        print('=====当前目录=====\n {}\n{}'.format(std_out.readlines()[0].strip(), ('=' * 18)))
        target = os.path.join(dest, src)
        src = os.path.join(os.getcwd(),src)
        bak = '{}.bak'.format(target)
        sftp = self.sftp

        print('源文件: ', src)
        print('目标文件:', target)
        try:
            sftp.stat(dest)
        except FileNotFoundError as _:
            print('远程路径不存在, 请检查')
        try:
            sftp.stat(target)
        except FileNotFoundError as _:
            #此处不可加权限探测语句，因原文件不存在!
            sftp.put(src, target)
            print('文件不存在, 已上传')
            return
        try:
            if sftp.stat(bak):
                sftp.remove(bak)
                mod = self.getmode(target)
                sftp.rename(target, bak)
                sftp.put(src, target)
                self.ssh.exec_command('chmod {} {}'.format(mod, target))
                print('文件存在, 已正确备份')
        except FileNotFoundError as _:
            mod = self.getmode(target)
            sftp.rename(target, bak)
            sftp.put(src, target)
            self.ssh.exec_command('chmod {} {}'.format(mod, target))
            print('备份文件不存在, 但已正确处理')


    def get(self, src ):
        """
        下载文件
        """
        if not src.startswith('/'):
            src = self.path + src
        target = os.path.join(os.getcwd(), os.path.basename(src))
        self.sftp.get(src, target)
        print('文件下载完成')


    def remove(self, des):
        """
        删除文件: 
        """
        if not des.startswith('/'):
            des = os.path.join(self.path + des)
        try:
            self.sftp.remove(des)
            print('成功删除')
        except FileNotFoundError :
            print('文件不存在, 请检查')


    def ls(self, des):
        """
        远程列目录: 
        """
        if not des.endswith('/'):
            des = des + '/'
        lst = self.sftp.listdir(des)
        for i in lst:
            print(i)


if __name__ == '__main__':
    client = scp()
    client.conn()
    try:
        if sys.argv[1] == 'put':
            # print('参数已接收', sys.argv)
            client.puts(sys.argv[2], sys.argv[3])
            print('上传完成.')
        elif sys.argv[1] == 'get':
            client.get(sys.argv[2])
        elif sys.argv[1] == 'remove':
            client.remove(sys.argv[2])
        elif sys.argv[1] == 'ls':
            client.ls(sys.argv[2])
        else:
            print('操作无效, 无此方法?')
    except IndexError as e:
        print('缺少参数?---{}'.format(sys.argv))
        if sys.argv[1] == 'put' and len(sys.argv) < 4:
            client.puts(sys.argv[2])
            print('上传成功')
