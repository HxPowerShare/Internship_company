import pymysql
import requests
from pyquery import PyQuery

# 创建列表存储字典
data_list = []


# 获取数据
def get_info():
    page = 68473
    while True:
        # 获取比赛选手详细信息的url
        url = 'https://m.wanplus.com/match/{}.html#data'.format(page)
        res = requests.get(url).content
        pqHtml = PyQuery(res.decode())
        # 30388
        # 67695
        # 68472
        # 测试30388-30665
        if page > 68557:
            break
        page += 1
        if pqHtml('title').text()[:2] != '20':
            continue
        if not pqHtml('div.bans_tx.fl p').text():
            continue
        print(page)
        # 存储战队一比赛信息
        a = 0
        b = 0
        str01 = ''
        for bans in pqHtml('div.las_box img').items():
            str01 += bans.attr('alt') + ' '
        for each in pqHtml('div.match_bans').items():
            data_dict = {}
            data_dict['bans'] = str01
            data_dict['league'] = pqHtml('div.matching_intro').text().split('>')[0]
            data_dict['battle'] = pqHtml('div.matching_intro').text().split('>')[1]
            data_dict['sessions'] = pqHtml('div.matching_intro').text().split()[-1]
            data_dict['team_name'] = pqHtml('div.bssj_top span.tl.bssj_tt1').text().split()[0]
            data_dict['url'] = url
            if a % 4 == 0:
                data_dict['player_name'] = pqHtml('div.bans_tx.fl p').text().split()[a]
                a += 1
                data_dict['role_name'] = pqHtml('div.bans_tx.fl p').text().split()[a]
                a += 1
                if a % 4 == 2:
                    for each01 in pqHtml('div.bans_m ul li span.tr').items():
                        if b % 4 == 0:
                            data_dict['KDA'] = pqHtml('div.bans_m ul li span.tr').text().split()[b]
                        elif b % 4 == 1:
                            data_dict['money'] = pqHtml('div.bans_m ul li span.tr').text().split()[b]
                        elif b % 4 == 2:
                            data_dict['output'] = pqHtml('div.bans_m ul li span.tr').text().split()[b]
                        elif b % 4 == 3:
                            data_dict['bear'] = pqHtml('div.bans_m ul li span.tr').text().split()[b]
                            b += 1
                            break
                        b += 1
            if a % 4 == 2:
                a += 2
            data_list.append(data_dict)
        # 存储战队二比赛信息
        a = 0
        b = 0
        for each in pqHtml('div.match_bans').items():
            data_dict = {}
            data_dict['bans'] = str01
            data_dict['league'] = pqHtml('div.matching_intro').text().split('>')[0]
            data_dict['battle'] = pqHtml('div.matching_intro').text().split('>')[1]
            data_dict['sessions'] = pqHtml('div.matching_intro').text().split()[-1]
            data_dict['team_name'] = pqHtml('div.bssj_top span.tr.bssj_tt3').text().split()[-1]
            data_dict['url'] = url
            if a % 4 == 0:
                a += 2
            if a % 4 == 2:
                data_dict['player_name'] = pqHtml('div.bans_tx.fl p').text().split()[a]
                a += 1
                data_dict['role_name'] = pqHtml('div.bans_tx.fl p').text().split()[a]
                a += 1
                for each02 in pqHtml('div.bans_m ul li span.tl').items():
                    if b % 4 == 0:
                        data_dict['KDA'] = pqHtml('div.bans_m ul li span.tl').text().split()[b]
                    elif b % 4 == 1:
                        data_dict['money'] = pqHtml('div.bans_m ul li span.tl').text().split()[b]
                    elif b % 4 == 2:
                        data_dict['output'] = pqHtml('div.bans_m ul li span.tl').text().split()[b]
                    elif b % 4 == 3:
                        data_dict['bear'] = pqHtml('div.bans_m ul li span.tl').text().split()[b]
                        b += 1
                        break
                    b += 1
            data_list.append(data_dict)


# 存储数据到数据库
def save_data():
    # 连接数据库
    database = 'kpl_history'
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db=database,
                           charset='utf8')
    get_info()
    cur = conn.cursor()
    # 数据写入
    into = 'INSERT INTO player_role_data(league,battle,sessions,bans,team_name,player_name,role_name,KDA,money,output,bear,url) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

    c = 0
    for each in data_list:
        value = (
            data_list[c]['league'], data_list[c]['battle'], data_list[c]['sessions'], data_list[c]['bans'],
            data_list[c]['team_name'], data_list[c]['player_name'], data_list[c]['role_name'], data_list[c]['KDA'],
            data_list[c]['money'], data_list[c]['output'], data_list[c]['bear'], data_list[c]['url'])
        # print(value)
        cur.execute(into, value)
        # 提交数据
        conn.commit()
        c += 1
    # 关闭数据库
    conn.close()


if __name__ == '__main__':
    save_data()
