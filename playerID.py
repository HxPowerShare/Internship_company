import requests
import pymysql
from pyquery import PyQuery

# 连接数据库
database = 'kpl_history'
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db=database, charset='utf8')
cur = conn.cursor()


def player_id():
    sql = 'SELECT ID,url FROM player_role_data WHERE player_id IS NULL'
    updateSql = 'UPDATE player_role_data SET player_id = %s WHERE ID = %s'
    while True:
        try:
            cur.execute(sql)
            results = cur.fetchone()
            url = results[1]
            res = requests.get(url).content
            pqHtml = PyQuery(res.decode())
            a = 0
            for each01 in pqHtml('div.bans_tx.fl p a').items():
                x = results[0]
                if a == 0:
                    val = (each01.attr('href')[-5:], x)
                    cur.execute(updateSql, val)
                if a == 4:
                    val = (each01.attr('href')[-5:], x + 1)
                    cur.execute(updateSql, val)
                if a == 8:
                    val = (each01.attr('href')[-5:], x + 2)
                    cur.execute(updateSql, val)
                if a == 12:
                    val = (each01.attr('href')[-5:], x + 3)
                    cur.execute(updateSql, val)
                if a == 16:
                    val = (each01.attr('href')[-5:], x + 4)
                    cur.execute(updateSql, val)
                if a == 2:
                    val = (each01.attr('href')[-5:], x + 5)
                    cur.execute(updateSql, val)
                if a == 6:
                    val = (each01.attr('href')[-5:], x + 6)
                    cur.execute(updateSql, val)
                if a == 10:
                    val = (each01.attr('href')[-5:], x + 7)
                    cur.execute(updateSql, val)
                if a == 14:
                    val = (each01.attr('href')[-5:], x + 8)
                    cur.execute(updateSql, val)
                if a == 18:
                    val = (each01.attr('href')[-5:], x + 9)
                    cur.execute(updateSql, val)
                a += 1
            conn.commit()
            print(x)
        except:
            print('end_player_id')
            break


conn.close()
