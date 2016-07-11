import os
import time

source ='d:\\tools\\autoruns'

target_dir = 'd:\\'

today = target_dir + os.sep + time.strftime('%Y%m%d')

now = time.strftime('%H_%M')

target = today + os.sep + now + '.zip'
if not os.path.exists(today):
    os.mkdir(today)
    print('Folder Sucessfully Created')

zip_command = 'd:\\tools' + os.sep +'zip -qr {0} {1}'.format(target, source)

if os.system(zip_command) == 0:
    print('成功')
else:
    print('Unsuccessful')
