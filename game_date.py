import requests
import pymysql
from pyquery import PyQuery

# 连接数据库
database = 'kpl_history'
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db=database, charset='utf8')
cur = conn.cursor()


def game_date():
    sql = 'SELECT ID,url FROM player_role_data WHERE date IS NULL'
    try:
        cur.execute(sql)
        results = cur.fetchall()
        for each in results:
            url = each[1]
            result = each[0]
            print(result)
            res = requests.get(url).content
            pqHtml = PyQuery(res.decode())
            a = 0
            for each_a in pqHtml('div.matching_intro a').items():
                a += 1
                if a == 2:
                    AimUrl = 'https://m.wanplus.com/' + each_a.attr('href')
                    AimRes = requests.get(AimUrl).content
                    AimPqHtml = PyQuery(AimRes.decode())
                    AimPqHtml('ul.match_mn1 p strong').remove()
                    data_dict = {}
                    data_dict['date'] = AimPqHtml('ul.match_mn1 p').text().split()[0]
                    data_dict['time'] = AimPqHtml('ul.match_mn1 p').text().split()[1]
                    data_dict['BO'] = AimPqHtml('ul.match_mn1 p').text().split()[-1]
                    updateSql = 'UPDATE player_role_data SET date = %s,time = %s,BO = %s WHERE ID = %s'
                    val = (data_dict['date'], data_dict['time'], data_dict['BO'], result)
                    cur.execute(updateSql, val)
                    conn.commit()
    except:
        print('end_game_date')


conn.close()
