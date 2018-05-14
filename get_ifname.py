#!/usr/bin/env python
#该脚本用来返回主机的主网卡的名字.原理是通过尝试连接公网IP,获得源IP,再通过它得到网卡名.
#需要下载ifaddr库: pip install ifaddr
import ifaddr
import socket

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


ip_addr = get_ip_address()
adapters = ifaddr.get_adapters()
for i in adapters:
  if i.ips[0].ip == ip_addr:
    print i.name

