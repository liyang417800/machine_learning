#coding:utf-8
"""
获取实时汇率
Created on Fri Oct 18 13:11:40 2013

@author: alala
"""

import httplib
import re
import MySQLdb
import datetime

URL = 'fx.cmbchina.com' #网站名
PATH = '/hq/'           #页面路径
HOST = 'localhost'      #数据库地址（ip）
DB = "money"            #数据库名称
USER = 'root'           #数据库用户名
PSWD = 'root'          #数据库密码

httpClient = None

currency={'人民币':'CNY','美元':'USD','欧元':'EUR','英镑':'GBP','澳大利亚元':'AUD','港币':'HKD','日元':'JPY'}
data = datetime.datetime.now().strftime('%Y-%m-%d')

try:
    #抓去网页内容
    httpClient = httplib.HTTPConnection(URL, 80, timeout=30)
    httpClient.request('GET', '/hq/')
    response = httpClient.getresponse()
    html = response.read()
    #print html

    #用正则表达式抓去汇率数据
    reg = re.compile(r"""
    <tr>\s*<td\s+class="fontbold">\s*(?P<name>\S+)\s*</td>\s*         #交易币
    <td\s+align="center">\s*(?P<unit>\d+)\s*</td>\s*                  #交易币单位
    <td\s+align="center"\s+class="fontbold">\s*(?P<base>\S+)\s*</td>\s*  #基本币
    <td\s*class="numberright">\s*(?P<midPrice>\d+\.\d+)\s*</td>\s*       #中间价
    <td\s*class="numberright">\s*(?P<sellPrice>\d+\.\d+)\s*</td>\s*                     #卖出价
    <td\s*class="numberright">\s*(?P<buyPrice1>\d+\.\d+)\s*</td>\s*                     #现汇买入价
    <td\s*class="numberright">\s*(?P<buyPrice2>\d+\.\d+)\s*</td>\s*                     #现钞买入价
    <td\s*align="center">\s*(?P<time>\d+:\d+:\d+)\s*</td>\s*                       #时间
    """, re.MULTILINE | re.X)
    rows = reg.findall(html)
    #打印汇率数据
    # for r in rows:
    #     print ','.join(map(str,r)), '\n'
    # print type(rows)
    #数据库操作
    #确保mysqldb已经安装，可以用下面的命令安装
    #pip install MySQL-python

    #建立和数据库系统的连接
    conn = MySQLdb.connect(host=HOST, user=USER,passwd=PSWD)

    #获取操作游标
    cursor = conn.cursor()
    #执行SQL,创建一个数据库.
    cursor.execute("CREATE DATABASE IF NOT EXISTS " + DB +" DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci")

    #选择数据库
    conn.select_db(DB);
    #执行SQL,创建一个数据表.
    cursor.execute("""CREATE TABLE IF NOT EXISTS exchange_rate(
                    name VARCHAR(50) COMMENT '交易币' ,
                    name_desc VARCHAR(50) COMMENT '交易币英文缩写',
                    unit INT COMMENT '交易币单位',
                    base VARCHAR(50) COMMENT '基本币',
                    base_desc VARCHAR(50) COMMENT '基本币英文缩写',
                    midPrice FLOAT COMMENT '中间价',
                    sellPrice FLOAT COMMENT '卖出价',
                    buyPrice1 FLOAT COMMENT '现汇买入价',
                    buyPrice2 FLOAT COMMENT '现钞买入价',
                    data DATE COMMENT '时间' ) """)
    records = []
    # print rows[0]




    for r in rows:
        if currency.get(r[0]):
            (name,unit,base,midPrice,sellPrice,buyPrice1,buyPrice2,time) = r
            record = (name,currency.get(name),int(unit),base,currency.get(base),float(midPrice),float(sellPrice),
                      float(buyPrice1),float(buyPrice2),data)
            records.append(record)

    cursor.execute("SET NAMES utf8")
    cursor.execute("SET CHARACTER_SET_CLIENT=utf8")
    cursor.execute("SET CHARACTER_SET_RESULTS=utf8")

    #批量插入当日汇率
    cursor.execute("delete from exchange_rate where data='%s' " %(data))
    cursor.executemany("insert into exchange_rate VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",records);
    conn.commit()

    # 关闭连接，释放资源
    cursor.close();

except Exception,e:
    print e
finally:
    if httpClient:
        httpClient.close()


