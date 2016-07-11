#--- coding: utf-8 ----
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('10.0.0.7', 9999))
print('Bined UDP on 9999...')
while True:
    data, addr = s.recvfrom(1024)
    print(('Recevied from %s:%s' % addr), data.decode('utf-8'))
    s.sendto(('Hello, %s!'% data.decode('utf-8')).encode('utf-8'), addr)
    # s.sendto(b'Hello, %s!' % data, addr)    #若解释器是3.5以上,可用这句,在bytes类型中直接插入str
