#!/usr/bin/env python
#coding:utf-8
#防篡改系统脚本.实时运行,用于实时监测目录是否发生改动(包括文件元数据),若发生改动会自动执行rysnc同步操作,拉取后端文件覆盖回来,并通过平台发送报警消息.注意:log_url, env变量,send_message方法没有通用性.
import logging
import datetime
import inotify.adapters
import os
import requests
import subprocess
from ConfigParser import SafeConfigParser
from copy import deepcopy


logging.basicConfig(
    format = '%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO,
    filename='/data/anti-tamper/anti-tamper.log'
)
log_url = 'http://192.168.66.105:8000/anti/tamper/log/create/'  #post
remote_ip = '192.168.30.149'
env = 'DEVELOP' #或 PRODUCT
local_path = '/data/tomcat-app/webapps/ROOT/'
remote_path = 'htdocs'


class Anti_tamper:
    def __init__(self, remote_ip):
        self.operation = ('IN_CREATE', 'IN_DELETE', 'IN_MODIFY', 'IN_ATTRIB', 'IN_DELETE_SELF', 'IN_MOVE_SELF', 'IN_MOVED_FROM', 'IN_MOVED_TO')
        self.conf_file = '/data/anti-tamper/anti-tamper.ini'
        self.remote_ip = remote_ip
        self.remote_path = 'htdocs'
        self.local_path = '/data/tomcat-app/webapps/ROOT/'
        self.except_paths = set()
        self.rsyn_cmd = ['/bash', '-lc', '/usr/bin/rsync', '-av', '--delete', '--exclude={%s}' % ','.join(list(self.except_paths)), '%s::%s' % ( self.remote_ip, self.remote_path), self.local_path]
        self.msg_template = [u'=====防篡改报警=====', u'主  机  名 : %s' % os.uname()[1]]
        self.message = deepcopy(self.msg_template)

    def read_conf(self):
        config = SafeConfigParser()
        config.read(self.conf_file)
        for k, v in config.defaults().items():
            if k == 'local_path':
                self.local_path = v
            elif k == 'remote_ip':
                self.remote_ip = v
            elif k == 'remote_path':
                self.remote_path = v
            elif 'except_path' in k:
                self.except_paths.add(v)

    def mk_sync_cmd(self):
        # self.rsyn_cmd = ['/bin/bash', '-lc','/usr/bin/rsync', '-av', '--delete', '--exclude={%s}' % ','.join(self.except_paths), '%s::%s' % ( self.remote_ip, self.remote_path), self.local_path]
        self.rsyn_cmd = ['/usr/bin/rsync', '-av', '--delete', '--exclude={%s}' % ','.join(self.except_paths), '%s::%s' % ( self.remote_ip, self.remote_path), self.local_path]

    def rync_files(self):
        try:
            # print 'Running command: ', ' '.join(self.rsyn_cmd)
            result = subprocess.Popen(self.rsyn_cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE).communicate()
            logging.warning(u'使用Rsync进行反篡改: ' + result[0] if result[0] else u'使用Rsync进行反篡改: ' + result[1])
            self.message.append(u"=====>使用Rsync进行反篡改 : ")
            self.message.append( result[0] if result[0] else result[1])
        except Exception as e:
            logging.warning(e)

    def send_message(self):
        sm = requests.session()
        data = {
            'work_no':'048423',
            'message':'\n'.join(self.message)
        }
        try:
            res = sm.get('http://kylin.niwodai.net/message/send/', params=data)
            logging.info('Response code of sending message: %s ' % res.status_code)
        except Exception as e:
            logging.error(e)
            self.message = deepcopy(self.msg_template)
        finally:
            self.message = deepcopy(self.msg_template)

    def main(self):
        self.read_conf()
        self.mk_sync_cmd()
        i = inotify.adapters.Inotify()
        i.add_watch(self.local_path )
        tramper = False

        try:
            for event in i.event_gen():
                if event is not None:
                    (header, type_names, watch_path, filename) = event
                    for attr in type_names:
                        if attr in self.operation:
                            logging.warning(u"动作=%s " u"监视路径=%s 文件名=%s", type_names, watch_path.decode('utf-8'), filename.decode('utf-8'))
                            self.message.append(u"时       间 : %s \n动       作 : %s \n监视路径 : [%s] \n文  件  名 : [%s]" % ( datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), type_names, watch_path.decode('utf-8'), filename.decode('utf-8')))
                            tramper = True
                    else:
                        if tramper == True:
                            #开始同步文件
                            self.rync_files()
                            #通过微信接口发送反篡改日志
                            self.send_message()
                            #通过麒麟接口发送反篡改日志
                            params = {
                                "env": "DEVELOP",
                                "hostname": "web_frontend",
                                "ip": "192.168.30.148",
                                "alarm_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                "action": type_names,
                                "path": os.path.join(watch_path, filename).decode('utf-8')
                            }
                            try:
                                res = requests.session().post(log_url, data=params, timeout=5)
                                if len(res.content) < 1024:
                                    logging.info(res.content)
                            except Exception as e:
                                logging.error(e)
                            self.rync_files()#再次同步文件,防止发报警期间出现文件变化
                            break
        finally:
            i.remove_watch(self.local_path)



if __name__ == '__main__':
    anti_tamper = Anti_tamper(remote_ip)
    while True:
        anti_tamper.main()

