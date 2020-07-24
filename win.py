import pymysql
import requests
from pyquery import PyQuery

database = 'kpl_history'
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db=database,
                       charset='utf8')
cur = conn.cursor()


def win():
    try:
        sql = 'SELECT ID,team_name,url FROM player_role_data WHERE win IS NULL'
        updateSql_win = 'UPDATE player_role_data SET win = 1 WHERE ID = %s'
        updateSql_lose = 'UPDATE player_role_data SET win = 0 WHERE ID = %s'
        cur.execute(sql)
        results = cur.fetchall()
        # [0]ID,[1]team_name,[2]url
        for each in results:
            # print(each[0], each[1], each[2])
            print(each[0])
            val = (each[0])
            url = each[2]
            res = requests.get(url).content
            pqHtml = PyQuery(res.decode())
            team_name01 = pqHtml('div.bssj_top span.tl.bssj_tt1').text().split()[0]
            team_win01 = pqHtml('div.bssj_top span.tl.bssj_tt1').text().split()[-1]
            team_name02 = pqHtml('div.bssj_top span.tr.bssj_tt3').text().split()[-1]
            team_win02 = pqHtml('div.bssj_top span.tr.bssj_tt3').text().split()[0]
            if each[1] == team_name01:
                if team_win01 == '胜':
                    cur.execute(updateSql_win, val)
                    conn.commit()
                else:
                    cur.execute(updateSql_lose, val)
                    conn.commit()
            elif each[1] == team_name02:
                if team_win02 == '胜':
                    cur.execute(updateSql_win, val)
                    conn.commit()
                else:
                    cur.execute(updateSql_lose, val)
                    conn.commit()
    except:
        print('end_win')


cur.close()
conn.close()
