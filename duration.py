import requests
from pyquery import PyQuery
import pymysql

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
# 连接数据库
database = 'kpl_history'
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db=database,
                       charset='utf8')
cur = conn.cursor()
sql = 'SELECT ID,url FROM player_role_data WHERE duration IS NULL'
update_sql = 'UPDATE player_role_data SET duration = %s WHERE ID = %s'
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
cur.close()
conn.close()
