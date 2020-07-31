# 用于获取各战队总数据，胜局/平局/负局
# 清空team_data表后运行
# 其中战队VgHow 0/0/10,LK 1/0/9
import requests
from pyquery import PyQuery
from Internship_company.KPL.team_data.conatants import team_league
import pymysql

header = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-length': '3999',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': 'wanplus_sid=df50052a40873deff0a89dae4ed48c49; UM_distinctid=1730db3beba2f7-01ff2edbf114b3-4353760-1fa400-1730db3bebbcd8; wp_pvid=769888400; gameType=6; wp_info=ssid=s4625214280; Hm_lvt_f69cb5ec253c6012b2aa449fb925c1c2=1594030331,1594083376,1594098240,1594100558; wanplus_token=77d962cb16304f5f93d1722702f8e2f8; wanplus_storage=k%2FUg5rCjZHaiKxm9zzaQl%2BnLA6Gz%2BXSTcsE2gl7y5Jq96IXrzfSBGCQw045lSehRKLE9zwNsxT4hH5VdpJiAgc%2FHlm310fdop7SHewnOIvY72R%2Fl%2Bf5p3C9TyVy%2B4fEPFbJqlxJd9Aw7vpmN589HFPk0DOcgIhxXlgFUa%2FagzZM; wanplus_csrf=_csrf_tk_268445179; isShown=1; CNZZDATA1275078652=1922056243-1593659181-https%253A%252F%252Fcn.bing.com%252F%7C1594108581; Hm_lpvt_f69cb5ec253c6012b2aa449fb925c1c2=1594110045',
    'origin': 'https://m.wanplus.com',
    'referer': 'https://m.wanplus.com/kog/playerstats',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'x-csrf-token': '352331259',
    'x-requested-with': 'XMLHttpRequest',
}

# 连接数据库
database = 'kpl_history'
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db=database,
                       charset='utf8')
cur = conn.cursor()
sql = 'INSERT IGNORE INTO team_data(team_id,team_name,historical_record,total_win,total_draw,total_lose) VALUES(%s,%s,%s,%s,%s,%s)'
# 查找数据
url = 'https://m.wanplus.com/ajax/stats/list'
for eid in team_league.league.items():
    data = {
        'start': 0,
        'length': 20,
        'eid': eid[1],
        'type': 'team',
        'gametype': 6,
    }

    res = requests.post(url, data=data, headers=header).json()
    league_lsts = res.get('data')
    for each in league_lsts:
        data_dict = {}
        data_dict['team_id'] = each.get('teamid')
        data_dict['team_name'] = each.get('teamname')
        # 展示进程
        print(each.get('teamid'))
        url01 = 'https://m.wanplus.com/kog/team/{}'.format(each.get('teamid'))
        res01 = requests.get(url01).content
        pqHtml = PyQuery(res01.decode())
        data_dict['historical_record'] = pqHtml('table.team_tbb dt').text().split()[0]
        data_dict['total_win'] = pqHtml('table.team_tbb dt').text().split()[0].split('/')[0]
        data_dict['total_draw'] = pqHtml('table.team_tbb dt').text().split()[0].split('/')[1]
        data_dict['total_lose'] = pqHtml('table.team_tbb dt').text().split()[0].split('/')[2]
        val = (data_dict['team_id'], data_dict['team_name'], data_dict['historical_record'], data_dict['total_win'],
               data_dict['total_draw'], data_dict['total_lose'])
        cur.execute(sql, val)
        conn.commit()
conn.close()
