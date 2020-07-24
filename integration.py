import requests
import pymysql
from pyquery import PyQuery

# 连接数据库
database = 'kpl_history'
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db=database, charset='utf8')
cur = conn.cursor()


# 获取时间信息
def get_game_date():
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


# 获取player_id
def get_player_id():
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


# 获取KDA
def get_KDA():
    sql = 'SELECT ID,KDA FROM player_role_data WHERE kill_num IS NULL'
    updateSql = 'UPDATE player_role_data SET kill_num = %s,die = %s,assists = %s WHERE ID = %s'
    try:
        cur.execute(sql)
        results = cur.fetchall()
        for each in results:
            val = (each[1].split('/')[0], each[1].split('/')[1], each[1].split('/')[2], each[0])
            cur.execute(updateSql, val)
        conn.commit()
    except:
        print('end_KDA')


def get_win():
    sql = 'SELECT ID,team_name,url FROM player_role_data WHERE win IS NULL'
    updateSql_win = 'UPDATE player_role_data SET win = 1 WHERE ID = %s'
    updateSql_lose = 'UPDATE player_role_data SET win = 0 WHERE ID = %s'
    try:
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


# 召唤师技能
def get_skill():
    skill_sql = 'SELECT ID,url FROM player_role_data WHERE summonerId IS NULL'
    update_skillSql = 'UPDATE player_role_data SET summonerId = %s WHERE ID = %s'
    while True:
        try:
            cur.execute(skill_sql)
            results = cur.fetchone()
            url = results[1]
            res = requests.get(url).content
            pqHtml = PyQuery(res.decode())
            end = str(results[0])
            print('skill:' + str(results[0]))
            a = 0
            pqHtml('div.bans_img a').remove()
            for each in pqHtml('div.bans_img img').items():
                # 队伍1
                if a == 0:
                    val = (each.attr('alt'), results[0])
                    cur.execute(update_skillSql, val)
                elif a == 2:
                    val = (each.attr('alt'), results[0] + 1)
                    cur.execute(update_skillSql, val)
                elif a == 4:
                    val = (each.attr('alt'), results[0] + 2)
                    cur.execute(update_skillSql, val)
                elif a == 6:
                    val = (each.attr('alt'), results[0] + 3)
                    cur.execute(update_skillSql, val)
                elif a == 8:
                    val = (each.attr('alt'), results[0] + 4)
                    cur.execute(update_skillSql, val)
                # 队伍2
                elif a == 1:
                    val = (each.attr('alt'), results[0] + 5)
                    cur.execute(update_skillSql, val)
                elif a == 3:
                    val = (each.attr('alt'), results[0] + 6)
                    cur.execute(update_skillSql, val)
                elif a == 5:
                    val = (each.attr('alt'), results[0] + 7)
                    cur.execute(update_skillSql, val)
                elif a == 7:
                    val = (each.attr('alt'), results[0] + 8)
                    cur.execute(update_skillSql, val)
                elif a == 9:
                    val = (each.attr('alt'), results[0] + 9)
                    cur.execute(update_skillSql, val)
                a += 1
            conn.commit()
        except:
            print('skill_end:' + end)
            break


# 出装
def get_equipment():
    equipment_sql = 'SELECT ID,url FROM player_role_data WHERE equipmentId1 IS NULL'
    while True:
        try:
            cur.execute(equipment_sql)
            results = cur.fetchone()
            url = results[1]
            res = requests.get(url).content
            pqHtml = PyQuery(res.decode())
            print('equipment:' + str(results[0]))
            end = str(results[0])
            b = 0
            for each in pqHtml('div.bans_bot').items():
                c = 1
                for each01 in each('img').items():
                    updateSql = 'UPDATE player_role_data SET equipmentId' + str(c) + '= %s WHERE ID = %s'
                    # 队伍1
                    if b == 0:
                        val = (each01.attr('alt'), results[0])
                        cur.execute(updateSql, val)
                        c += 1
                    elif b == 2:
                        val = (each01.attr('alt'), results[0] + 1)
                        cur.execute(updateSql, val)
                        c += 1
                    elif b == 4:
                        val = (each01.attr('alt'), results[0] + 2)
                        cur.execute(updateSql, val)
                        c += 1
                    elif b == 6:
                        val = (each01.attr('alt'), results[0] + 3)
                        cur.execute(updateSql, val)
                        c += 1
                    elif b == 8:
                        val = (each01.attr('alt'), results[0] + 4)
                        cur.execute(updateSql, val)
                        c += 1
                    # 队伍2
                    elif b == 1:
                        val = (each01.attr('alt'), results[0] + 5)
                        cur.execute(updateSql, val)
                        c += 1
                    elif b == 3:
                        val = (each01.attr('alt'), results[0] + 6)
                        cur.execute(updateSql, val)
                        c += 1
                    elif b == 5:
                        val = (each01.attr('alt'), results[0] + 7)
                        cur.execute(updateSql, val)
                        c += 1
                    elif b == 7:
                        val = (each01.attr('alt'), results[0] + 8)
                        cur.execute(updateSql, val)
                        c += 1
                    elif b == 9:
                        val = (each01.attr('alt'), results[0] + 9)
                        cur.execute(updateSql, val)
                        c += 1
                b += 1
            conn.commit()
        except:
            print('equipment_end:' + end)
            break


# 获取时长
def get_duration():
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-length': '28',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': '_uab_collina=159374546503722904732232; wanplus_sid=df50052a40873deff0a89dae4ed48c49; UM_distinctid=1730db3beba2f7-01ff2edbf114b3-4353760-1fa400-1730db3bebbcd8; wp_pvid=769888400; wanplus_token=77d962cb16304f5f93d1722702f8e2f8; wanplus_storage=k%2FUg5rCjZHaiKxm9zzaQl%2BnLA6Gz%2BXSTcsE2gl7y5Jq96IXrzfSBGCQw045lSehRKLE9zwNsxT4hH5VdpJiAgc%2FHlm310fdop7SHewnOIvY72R%2Fl%2Bf5p3C9TyVy%2B4fEPFbJqlxJd9Aw7vpmN589HFPk0DOcgIhxXlgFUa%2FagzZM; isShown=1; gameType=6; wanplus_csrf=_csrf_tk_268445179; wp_info=ssid=s4332280560; Hm_lvt_f69cb5ec253c6012b2aa449fb925c1c2=1595474022,1595474951,1595476193,1595484562; CNZZDATA1275078652=1922056243-1593659181-https%253A%252F%252Fcn.bing.com%252F%7C1595490886; Hm_lpvt_f69cb5ec253c6012b2aa449fb925c1c2=1595492912',
        'origin': 'https://m.wanplus.com',
        'referer': 'https://m.wanplus.com/schedule/26249.html',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'x-csrf-token': '352331259',
        'x-requested-with': 'XMLHttpRequest',
    }
    json_url = 'https://m.wanplus.com/schedule/getmatch'
    sql = 'SELECT ID,url FROM player_role_data WHERE duration IS NULL'
    update_sql = 'UPDATE player_role_data SET duration = %s WHERE ID = %s'
    try:
        cur.execute(sql)
        results = cur.fetchall()
        for each in results:
            print(each[0])
            matchid = each[1][-15:-10]
            data = {
                '_gtk': '352331259',
                'matchid': matchid,
            }
            rep = requests.post(json_url, data=data, headers=headers).json()
            duration_list = rep.get('data')
            pqHtml = PyQuery(duration_list)
            duration = pqHtml('div.las_midd').text().split('长')[-1]
            val = (duration, each[0])
            cur.execute(update_sql, val)
            conn.commit()
    except:
        print('end_duration')


if __name__ == '__main__':
    get_game_date()
    get_player_id()
    get_KDA()
    get_win()
    get_skill()
    get_equipment()
    get_duration()
    cur.close()
    conn.close()
