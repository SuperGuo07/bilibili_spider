import requests
import json
import csv
import pandas as pd
from fake_useragent import UserAgent

requests.packages.urllib3.disable_warnings()#忽视InsecureRequestWarning警告



# 随机ip代理获取
PROXY_POOL_URL = 'http://localhost:5555/random'
session=requests.Session()  # session会话

#代理字典，类型为http，使用其后代理IP，类型为Https，使用其后代理。
proxies = {
    "http":"http://78.141.201.90:33723",
    "https":"http://78.141.201.90:33723",
}
#获取代理IP，并打印
prox=requests.get(PROXY_POOL_URL).text
print('代理IP为：'+prox)

#proxies字典重新赋值
proxies["http"],proxies["https"]=prox,prox

ua = UserAgent()

# 爬虫地址
alphabet = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
def dec(x):  # BV号转换成AV号
    r = 0
    for i, v in enumerate([11, 10, 3, 8, 4, 6]):
        r += alphabet.find(x[v]) * 58 ** i
    return (r - 0x2_0840_07c0) ^ 0x0a93_b324


bid = input("input video bv number:")
aid = dec(bid)
url = r'https://api.bilibili.com/x/web-interface/archive/stat?aid=' + str(aid)
# 携带cookie进行访问
headers = {
'User-Agent':ua.random,
'Accept': 'text/html',
'Cookie': "_uuid=1DBA4F96-2E63-8488-DC25-B8623EFF40E773841infoc; buvid3=FE0D3174-E871-4A3E-877C-A4ED86E20523155831infoc; LIVE_BUVID=AUTO8515670521735348; sid=l765gx48; DedeUserID=33717177; DedeUserID__ckMd5=be4de02fd64f0e56; SESSDATA=cf65a5e0%2C1569644183%2Cc4de7381; bili_jct=1e8cdbb5755b4ecd0346761a121650f5; CURRENT_FNVAL=16; stardustvideo=1; rpdid=|(umY))|ukl~0J'ulY~uJm)kJ; UM_distinctid=16ce0e51cf0abc-02da63c2df0b4b-5373e62-1fa400-16ce0e51cf18d8; stardustpgcv=0606; im_notify_type_33717177=0; finger=b3372c5f; CURRENT_QUALITY=112; bp_t_offset_33717177=300203628285382610"
}
# 获取url

response = session.get(url, timeout=30, headers=headers,proxies=proxies,verify=False)
session.close()
#可以根据状态码判断是否获取成功，200即获取成功
print('网页状态码为:'+str(response.status_code))

text = response.text
jsonobj = json.loads(text)

# 从Json对象获取视频基本信息并转入词典中
video_dict = {'aid': jsonobj['data']['aid'],
              'bvid': jsonobj['data']['bvid'],
              'view': jsonobj['data']['view'],
              'danmuku_num': jsonobj['data']['danmaku'],
              'reply_num': jsonobj['data']['reply'],
              'favorite_num': jsonobj['data']['favorite'],
              'coin_num': jsonobj['data']['coin'],
              'share_num': jsonobj['data']['share'],
              'like_num': jsonobj['data']['like']
              }
dataFrame = pd.DataFrame(video_dict,
                         columns=['aid', 'bvid', 'view', 'danmuku_num', 'reply_num', 'favorite_num', 'coin_num',
                                  'share_num', 'like_num'], index=[0])

print(video_dict)
print(dataFrame)
# 转换为csv格式存储
dataFrame.to_csv("test.csv", index=False)

