# 用于获取所有全部比赛战队比分情况
# 直接运行即可
import requests
import pymysql
from pyquery import PyQuery

# 连接数据库
database = 'kpl_history'
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db=database,
                       charset='utf8')
cur = conn.cursor()

score_headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'wanplus_sid=df50052a40873deff0a89dae4ed48c49; UM_distinctid=1730db3beba2f7-01ff2edbf114b3-4353760-1fa400-1730db3bebbcd8; wp_pvid=769888400; wanplus_token=77d962cb16304f5f93d1722702f8e2f8; wanplus_storage=k%2FUg5rCjZHaiKxm9zzaQl%2BnLA6Gz%2BXSTcsE2gl7y5Jq96IXrzfSBGCQw045lSehRKLE9zwNsxT4hH5VdpJiAgc%2FHlm310fdop7SHewnOIvY72R%2Fl%2Bf5p3C9TyVy%2B4fEPFbJqlxJd9Aw7vpmN589HFPk0DOcgIhxXlgFUa%2FagzZM; isShown=1; gameType=6; wanplus_csrf=_csrf_tk_268445179; wp_info=ssid=s8682624982; Hm_lvt_f69cb5ec253c6012b2aa449fb925c1c2=1595815332,1595816690,1595840705,1595901988; CNZZDATA1275078652=1922056243-1593659181-https%253A%252F%252Fcn.bing.com%252F%7C1595907765; Hm_lpvt_f69cb5ec253c6012b2aa449fb925c1c2=1595908211',
    'referer': 'https://m.wanplus.com/kog/team/4458',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'x-csrf-token': '352331259',
    'x-requested-with': 'XMLHttpRequest',
}

date_headers = {
    'cookie': 'wanplus_token=51ff3f33bd908b4a82ded7a04d6b4f8e; wanplus_storage=lf4m67eka3o; wanplus_sid=e10693d5f99501205aabb2423209a79c; wanplus_csrf=_csrf_tk_1749651587; UM_distinctid=173936d3c19277-0d8e3aa9b979d2-3d644601-1fa400-173936d3c1a88f; CNZZDATA1275078652=22555735-1595902361-%7C1595902361; wp_pvid=8409101905; wp_info=ssid=s1153002494; gameType=6; Hm_lvt_f69cb5ec253c6012b2aa449fb925c1c2=1595906289; Hm_lpvt_f69cb5ec253c6012b2aa449fb925c1c2=1595906517',
    'x-csrf-token': '1833537667',
}

select_sql = 'SELECT team_id FROM team_data'
cur.execute(select_sql)
team_ids = cur.fetchall()
for team_id in team_ids:
    team_url = 'https://m.wanplus.com/kog/team/{}'.format(team_id[0])
    page = 1
    while True:
        try:
            # 进度标志
            print('team_id:' + str(team_id[0]) + '    page:' + str(page))
            score_url = 'https://m.wanplus.com/ajax/team/recent?isAjax=1&teamId={}'.format(
                team_id[0]) + '&gameType=6&objTeamId=0&page={}&totalPage=30&totalItems=600&_gtk=352331259'.format(page)
            page += 1
            score_res = requests.get(score_url, headers=score_headers).json()
            race_lists = score_res.get('data')
            for each in race_lists:
                data_dic = {}
                data_dic['url'] = team_url
                data_dic['scheduleid'] = each.get('scheduleid')
                data_dic['eid'] = each.get('eid')
                data_dic['stageid'] = each.get('stageid')
                data_dic['team_name1'] = each.get('oneseedname')
                data_dic['team_name2'] = each.get('twoseedname')
                data_dic['point1'] = each.get('onewin')
                data_dic['point2'] = each.get('twowin')
                date_url = 'https://m.wanplus.com/ajax/event/block?eventId={}'.format(
                    data_dic['eid']) + '&stageId={}'.format(
                    data_dic['stageid']) + '&sheduleId={}'.format(data_dic['scheduleid']) + '&_gtk=352331259'
                date_res = requests.get(date_url, headers=date_headers).content
                pqHtml = PyQuery(date_res.decode())
                data_dic['league'] = pqHtml.text().split('\n')[0]
                data_dic['datetime'] = pqHtml.text().split('\n')[1]
                data_dic['date'] = pqHtml.text().split('\n')[1].split()[0]
                data_dic['time'] = pqHtml.text().split('\n')[1].split()[-1]
                data_dic['BO'] = pqHtml.text().split('\n')[-1][-1]
                insert_sql = 'INSERT IGNORE INTO match_schedule(datetime,date,time,BO,team_name1,team_name2,point1,point2,league,url) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                val = (data_dic['datetime'], data_dic['date'], data_dic['time'], data_dic['BO'], data_dic['team_name1'],
                       data_dic['team_name2'], data_dic['point1'], data_dic['point2'], data_dic['league'],
                       data_dic['url'])
                cur.execute(insert_sql, val)
                conn.commit()
        except:
            break

cur.close()
conn.close()
