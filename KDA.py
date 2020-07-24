import pymysql

database = 'kpl_history'
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db=database, charset='utf8')
cur = conn.cursor()


def KDA():
    try:
        sql = 'SELECT ID,KDA FROM player_role_data WHERE kill_num IS NULL'
        updateSql = 'UPDATE player_role_data SET kill_num = %s,die = %s,assists = %s WHERE ID = %s'
        cur.execute(sql)
        results = cur.fetchall()
        for each in results:
            val = (each[1].split('/')[0], each[1].split('/')[1], each[1].split('/')[2], each[0])
            cur.execute(updateSql, val)
        conn.commit()
    except:
        print('end_KDA')


cur.close()
conn.close()
