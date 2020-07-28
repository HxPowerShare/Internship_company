# 用于获取各赛季选手信息
# 每有新赛季开始时运行一次即可，运行时需要清空player_list表
import requests
import pymysql
from KPL.team_data.conatants import team_league

# 连接数据库
database = 'kpl_history'
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db=database,
                       charset='utf8')
cur = conn.cursor()

# 构建请求头
headers = {
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

for eid in team_league.league.items():
    # 展示进度
    print(eid[1])
    data = {
        'start': 0,
        'length': 200,
        'eid': eid[1],
        'type': 'player',
        'gametype': 6,
    }

    url = 'https://m.wanplus.com/ajax/stats/list'
    req = requests.post(url, data=data, headers=headers).json()
    player_lsts = req.get('data')

    if player_lsts:
        for player_lst in player_lsts:
            data_dict = {}
            data_dict['playerid'] = player_lst.get('playerid')
            data_dict['playername'] = player_lst.get('playername')
            data_dict['teamid'] = player_lst.get('teamid')
            data_dict['teamname'] = player_lst.get('teamname')
            data_dict['league'] = eid[0]
            into = "INSERT INTO player_list(playerId,nick,teamId,teamName,league) VALUES(%s,%s,%s,%s,%s)"
            values = (data_dict['playerid'], data_dict['playername'], data_dict['teamid'], data_dict['teamname'],
                      data_dict['league'])
            cur.execute(into, values)
            conn.commit()
cur.close()
conn.close()
