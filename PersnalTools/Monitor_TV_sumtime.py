"""
IP在线监控工具, 原意用于监控电视(乐视,可连接无线网)开机时间, 防止老年人看电视过久影响健康.
功能: 持续监控IP, 若上线即开始计时, 并向Windows主机发送提醒消息. Windows可看到弹出的提示框; IP下线亦提醒.
      若在线持续1.5小时或一天内超过4小时, 也会发出提醒.
      远端或监控端短时间意外断电, 重新运行脚本可继续运行不受影响.
      单例运行, 多次执行只开一个进程.
该工具是本人初作, 存在一定冗余代码和可改进之处, 后面会用类方式改造下. 增加强壮度.
"""

#coding:utf-8
import datetime
import pyping
import sqlite3
import time
import winrm
import tendo.singleton

me = tendo.singleton.SingleInstance()

mark = {'online':0,
        'count':0,
        'closed':1,
        'timer':0
        }
today = datetime.datetime.today().strftime('%Y-%m-%d')
print(today)

def pingscan():
    t_start = time.time()
#    print('t_start is:', t_start)
    while True :
        try:
            p = pyping.ping('10.1.1.1', timeout=3000, count=4)
        except Exception as e:
            print(e)
        if p.avg_rtt:
            time.sleep(7)
            t_stop = time.time()

            global today
            today = datetime.datetime.today().strftime('%Y-%m-%d')
            if mark['count'] == 0:
#                print('已开机')
#                alarm('began')
                markdb('mark_start')
            mark['online'] += (t_stop - t_start)
#            print('mark.online is:', mark['online'])
            if mark['closed'] > 0:
                alarm('began')
                print('已开机')
                mark['closed'] = 0
            if mark['online'] > 606:#若online在线超过10分钟,在DB中标记最新时间戳.
                 markdb('cycle_mark')
                 mark['online'] = 6

            mark['count'] += (t_stop - t_start)
 #           print('mark.count is:', mark['count'])
            t_start = t_stop
            alarm()
 #           print('+1count=',mark['count'],'online=',mark['online'],'close=',mark['closed'])
        else:
            time.sleep(10)
            t_stop = time.time()
            if mark['closed'] == 0:
                alarm('closed')
                print('已关机')
            mark['closed'] += (t_stop - t_start)
            t_start = t_stop
        if mark['closed'] > 300 and mark['online'] != 0:#可加 and count > 10分钟
            mark['online'] = 0
            writedb()
            mark['count'] = 0
            print('Wrote DB and set count to 0 successfully')



def markdb(x):
    """
    每15分钟写一次数据库
    """
    with sqlite3.connect('/root/py2study/test.db') as db:
        select_date = db.execute("select date from sumtime")
        date_list = [str(i[0]) for i in select_date]
        if today not in date_list:
            db.execute("insert into sumtime(id, date, start, end, sumtime) values({0},'{1}', 0, 0, 0)".format((len(date_list)), today))
            db.commit()
        if x == 'cycle_mark':
            db.execute("update sumtime set end = '{0}' where date='{1}'".format(time.time(), today))
            db.commit()
  #         print(list(db.execute("select end from sumtime where date ='{0}'".format(today))))
  #         print('db commited')
        elif x == 'mark_start':
            db.execute("update sumtime set start = '{0}' where date='{1}'".format(time.time(), today))
            db.commit()

def writedb():
    """
    每确定一段使用时间,写一次使用时间字段
    """
  #  print(' '.join(('writedbing','count is ', str(mark['count']))))
    with sqlite3.connect('/root/py2study/test.db') as db:
        #下面查询已有几个时间段记录,并将新记录写入最后的一个
        select_date = db.execute("select date from sumtime")
        date_list = [str(i[0]) for i in select_date]
        if today not in date_list:
            db.execute("insert into sumtime(id, date, start, end, sumtime) values({0},'{1}', 0, 0, 0)".format((len(date_list)), today))
            db.commit()
        times = db.execute("select t0, t1, t2, t3, t4, t5, t6, t7, t8, t9  from sumtime where date='{0}'".format(today))
        print('Step 1')
        times_count = 0
        for ins in [x for x in times][0][0:9]:
            if ins is not None:
                times_count += 1
                continue
            db.execute("update sumtime set t{0} = {1} where date='{2}'".format(times_count, mark['count'], today))
  #     print('Setp 2 succeed')
        #下面是更新sumtime段的总时间值.先获取原sumtime值,可能为空.后面跟判断语句
        last_sum = list(db.execute("select sumtime from sumtime where date = '{0}'".format(today)))[-1][0]
        if last_sum is None:
            sumtime = mark['count']
        else:
            sumtime = mark['count'] + last_sum
        db.execute("update sumtime set sumtime = {0},start = 0, end = 0 where date ='{1}'".format(sumtime,today))
  #      print('Step 3 succeed')
        db.commit()

def alarm(arg=None):
    """
    统计每个段和总时间,报警,并通过winrm发送消息
    """
    try:
        opensession = winrm.Session('10.1.1.7', auth=('administrator','admin123'))
        now = time.time()
        if arg == 'began':
            opensession.run_cmd('msg Robert 已开机. ')
        elif arg == 'closed':
            opensession.run_cmd('msg Robert 已关机. ')
        elif arg is None:
            with sqlite3.connect('/root/py2study/test.db') as db:
                sumtime = list(db.execute("select sumtime from sumtime where date = '{0}'".format(today)))[-1][0]
                if mark['timer'] < now and ((sumtime + mark['count']) > 13800 or mark['count'] > 4800):
                    nowtime = datetime.datetime.now()
                    if mark['count'] < 13800:
                        opensession.run_cmd('msg Robert 本次开机时间已达1.5小时.当前时间:{0} '.format(nowtime))
                    else:
                        opensession.run_cmd('msg Robert 当前时间已达4小时.当前时间:{0}'.format(nowtime))
                    mark['timer'] += (600 + now)
    except Exception as ex:
        print('alarm error:', ex)


def dbupdate():
    """
    意外关机,初始化DB和count
    """
    with sqlite3.connect('/root/py2study/test.db') as db:
        select_date = db.execute("select date from sumtime")
        date_list = [str(i[0]) for i in select_date]
        print(date_list)
        if today not in date_list:
            db.execute("insert into sumtime(id, date, start, end, sumtime) values({0},'{1}', 0, 0, 0)".format((len(date_list)), today))
            db.commit()
        else:
            points = [y for y in db.execute("select start, end from sumtime where date = '{0}'".format(today))]
            start = points[0][0]
            end = points[0][1]
            print(points)
            print('start=',start)
            print('end=',end)
            if (start != 0) and (end != 0):
                mark['count'] = end - start
                print('count=',mark['count'])
            elif (start != 0) and (end == 0):
                mark['count'] = time.time() - start
                print('count=', mark['count'])
if __name__ == '__main__':
    dbupdate()
    pingscan()




