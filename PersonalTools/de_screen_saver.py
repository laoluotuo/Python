#!python3
#本脚本用于防止屏保自动运行.可用于有强制屏保域策略的Windows系统,原理是每分钟模拟键盘操作,按下ScrollLock键
#将脚本更名为pyw,可使脚本运行在后台
#脚本运行在python3下,需要安装win32ext,win32gui等win32模块

import win32api, time, win32con
while True:
        try:
            time.sleep(60)
            print( "Hmm.. let's see what we have..")
            win32api.keybd_event(win32con.VK_SCROLL, 0, 0, 0)
            win32api.keybd_event(win32con.VK_SCROLL, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.1)
            win32api.keybd_event(win32con.VK_SCROLL, 0, 0, 0)
            win32api.keybd_event(win32con.VK_SCROLL, 0, win32con.KEYEVENTF_KEYUP, 0)
        except Exception as e:
            print(e)
