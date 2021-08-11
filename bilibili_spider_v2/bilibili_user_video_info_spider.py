import pymysql
import requests
import json
import csv
import pandas as pd
from fake_useragent import UserAgent
from bilibili_api import user,sync

requests.packages.urllib3.disable_warnings()#忽视InsecureRequestWarning警告


def get_user_info(video_url,fans_url,play_and_like_url):
    session = requests.Session()  # session会话

    # # 随机ip代理获取
    # PROXY_POOL_URL = 'http://localhost:5555/random'
    #
    #
    # # 代理字典，类型为http，使用其后代理IP，类型为Https，使用其后代理。
    # proxies = {
    #     "http": "http://78.141.201.90:33723",
    #     "https": "http://78.141.201.90:33723",
    # }
    # # 获取代理IP，并打印
    # prox = requests.get(PROXY_POOL_URL).text
    # print('代理IP为：' + prox)
    #
    # # proxies字典重新赋值
    # proxies["http"], proxies["https"] = prox, prox


    ua = UserAgent()
    # 携带cookie进行访问
    headers = {
    'User-Agent':ua.random,
    'Accept': 'text/html',
    'Cookie': "fingerprint=3764180791391f01326c0049db5786da; buvid_fp=55049C08-1A84-48FC-940D-974D832D316913438infoc; buvid_fp_plain=42EF3D6C-0A61-4FDB-8577-446F0F897CAE13426infoc; _uuid=0C638565-F88F-147A-7AEA-8FC12A956FDB34242infoc; buvid3=55049C08-1A84-48FC-940D-974D832D316913438infoc; fingerprint=02eb47712d0cc5aac50b5c0f8ae491c1; buvid_fp_plain=F79DFCA8-7DAD-439B-AA1C-031BECD325A534780infoc; SESSDATA=4f66b417%2C1641187523%2Cb3a20%2A71; bili_jct=d02579d1f1b8471a8efc04a0fe2220fc; DedeUserID=11305147; DedeUserID__ckMd5=6bba7b739c47ac15; sid=4x10278u; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(m~lJkm)k~0J'uYklYJllJ~; PVID=1; bsource=search_bing; bfe_id=1bad38f44e358ca77469025e0405c4a6"
    }
    play_and_like_response = session.get(play_and_like_url, timeout=30, headers=headers,verify=False)

    video_response = session.get(video_url, timeout=30, headers=headers,verify=False)
    fans_response = session.get(fans_url, timeout=30, headers=headers,verify=False)

    session.close()
    # 可以根据状态码判断是否获取成功，200即获取成功
    print('video_response网页状态码为:' + str(video_response.status_code))
    print('fans_response网页状态码为:' + str(fans_response.status_code))
    print('play_and_like_response网页状态码为:' + str(play_and_like_response.status_code))

    play_and_like_text = play_and_like_response.text
    video_text = video_response.text
    fans_text = fans_response.text

    jsonplayandlike = json.loads(play_and_like_text)
    jsonobj = json.loads(video_text)
    jsonfans = json.loads(fans_text)

    # print(jsonplayandlike)
    video_list = []

    # 从Json对象获取视频基本信息并转入词典中
    video_count = len(jsonobj['data']['list']['vlist'])
    # print(video_count)
    data = []
    dataFrame = pd.DataFrame(columns=['comment_count', 'type_id', 'play', 'pic', 'description', 'title', 'author',
                                      'mid', 'created', 'video_length', 'video_bullet_screen', 'aid', 'bvid','total_fans_count','total_view', 'total_likes'], index=[0])
    for i in range(video_count):

        # video_data = []
        #
        # comment_count = jsonobj['data']['list']['vlist'][i]['comment'],
        # type_id = jsonobj['data']['list']['vlist'][i]['typeid'],
        # play = jsonobj['data']['list']['vlist'][i]['play'],
        # pic = jsonobj['data']['list']['vlist'][i]['pic'],
        # description = jsonobj['data']['list']['vlist'][i]['description'],
        # title = jsonobj['data']['list']['vlist'][i]['title'],
        # author = jsonobj['data']['list']['vlist'][i]['author'],
        # mid = jsonobj['data']['list']['vlist'][i]['mid'],
        # created = jsonobj['data']['list']['vlist'][i]['created'],
        # length = jsonobj['data']['list']['vlist'][i]['length'],
        # video_review = jsonobj['data']['list']['vlist'][i]['video_review'],
        # aid = jsonobj['data']['list']['vlist'][i]['aid'],
        # bvid = jsonobj['data']['list']['vlist'][i]['bvid']

        # video_data.append(comment_count)
        # video_data.append(type_id)
        # video_data.append(play)
        # video_data.append(pic)
        # video_data.append(description)
        # video_data.append(title)
        # video_data.append(author)
        # video_data.append(mid)
        # video_data.append(created)
        # video_data.append(length)
        # video_data.append(video_review)
        # video_data.append(aid)
        # video_data.append(bvid)
        #
        # data.append(video_data)

        # wb = openpyxl.load_workbook(
        #     r"D:\Work\spider_data\douyin_spider_data\douyin 视频信息spider 3.xlsx")  # (r"D:\Work\spider_data\douyin_spider_data" + "\\" +"douyin_spider" + ".xlsx")
        # ws = wb.active

        # fans_dict = {
        #     'total_fans_count': jsonfans['data']['follower']
        # }

        video_dict = {
            'comment_count': jsonobj['data']['list']['vlist'][i]['comment'],
            'type_id': jsonobj['data']['list']['vlist'][i]['typeid'],
            'play': jsonobj['data']['list']['vlist'][i]['play'],
            'pic': jsonobj['data']['list']['vlist'][i]['pic'],
            'description': jsonobj['data']['list']['vlist'][i]['description'],
            'title': jsonobj['data']['list']['vlist'][i]['title'],
            'author': jsonobj['data']['list']['vlist'][i]['author'],
            'mid': jsonobj['data']['list']['vlist'][i]['mid'],
            'created': jsonobj['data']['list']['vlist'][i]['created'],
            'video_length': jsonobj['data']['list']['vlist'][i]['length'],
            'video_bullet_screen': jsonobj['data']['list']['vlist'][i]['video_review'],
            'aid': jsonobj['data']['list']['vlist'][i]['aid'],
            'bvid': jsonobj['data']['list']['vlist'][i]['bvid'],
            'total_fans_count': jsonfans['data']['follower'],
            'total_view': jsonplayandlike['data']['archive']['view'],
            'total_likes': jsonplayandlike['data']['likes']
        }

        dataFrame.loc[i] = video_dict


        # play_and_like_dict = {
        #     'total_like_count': jsonplayandlike['data']['likes'],
        #     'total_play_count': jsonplayandlike['data']['archive']['view']
        # }
        # print(play_and_like_dict)


        # print(fans_dict)

    # # 转换为csv格式存储
    # dataFrame.to_csv("video_test.csv", index=False,encoding='utf-8-sig')

    return dataFrame

def info_to_db(video_info):


    # 建立数据库连接
    db_241 = pymysql.connect(host="192.168.50.241",user="gsc",password="gsc123",database="jj_database" )
    db_213 = pymysql.connect(host="192.168.50.213",user="guo",password="123456",database="test1" )
    cursor = db_213.cursor()

    # print(video_info)

    for i in range(len(video_info)):
        comment_count = video_info["comment_count"][i]
        type_id = video_info["type_id"][i]
        play = video_info["play"][i]
        pic = video_info["pic"][i]
        description = video_info["description"][i]
        title = video_info["title"][i]
        author = video_info["author"][i]
        mid = video_info["mid"][i]
        created = video_info["created"][i]
        video_length = video_info["video_length"][i]
        video_bullet_screen = video_info["video_bullet_screen"][i]
        aid = video_info["aid"][i]
        bvid = video_info["bvid"][i]
        total_fans_count = video_info["total_fans_count"][i]
        total_view = video_info["total_view"][i]
        total_likes = video_info["total_likes"][i]

        # print(comment_count)
        # print(type_id)
        # print(play)

        # sql = "INSERT INTO bilibili_video_info(comment_count, type_id, play,pic, " \
        #       "description,title, author, mid,created,length,video_bullet_screen,aid,bvid,total_fans_count " \
        #       ",total_view,total_likes) values({},{},{},{},{},{},{},{},{},{},{},{},{}," \
        #       "{},{},{})".format(comment_count, '\'' + type_id + '\'', play,  '\'' + pic + '\'', '\'' + description + '\'', '\'' + title + '\'',
        #                    '\'' + author + '\'', '\'' + mid + '\'','\'' + created + '\'','\'' + length  + '\'',
        #                    video_bullet_screen, '\'' + aid  + '\'' , '\'' + bvid + '\'',total_fans_count, total_view, total_likes)

        # sql1 = "INSERT INTO bilibili_video_info(comment_count, type_id, play,pic, " \
        #        "description,title, author, mid,created,video_length,video_bullet_screen,aid,bvid,total_fans_count " \
        #        ",total_view,total_likes) values({},{},{},{},{},{},{},{},{},{},{},{},{}," \
        #        "{},{},{})".format(comment_count, type_id, play, pic, description, title, author, mid, created, video_length, video_bullet_screen, aid, bvid, total_fans_count, total_view, total_likes)
        sql2 = "INSERT INTO bilibili_video_info(comment_count, type_id, play,pic, description,title, author, mid," \
               "created,video_length,video_bullet_screen,aid,bvid,total_fans_count ,total_view,total_likes) " \
               "values({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{})".format(comment_count, type_id, play, '\'' +
                                                                                pic + '\'', '\'' + description + '\'',
                                                                                '\'' + title + '\'', '\'' + author +
                                                                                '\'', mid, created, '\'' + video_length
                                                                                + '\'', video_bullet_screen, aid, '\'' +
                                                                                bvid + '\'', total_fans_count,
                                                                                total_view, total_likes)
        cursor.execute(sql2)
        db_213.commit()
    cursor.close()
    print("db done")







if __name__ == '__main__':

    video_url_head = r'https://api.bilibili.com/x/space/arc/search?mid='
    fans_url_head = r'https://api.bilibili.com/x/relation/stat?vmid='
    play_and_like_head = r'http://api.bilibili.com/x/space/upstat?mid='
    # play_url = 'http://api.bilibili.com/x/space/upstat?mid='


    uid1 = 309947633 #43536   也是mid

    user_dict = {"亦栖设计": uid1}

    for k in user_dict:
        video_url = video_url_head + str(user_dict[k])
        fans_url = fans_url_head + str(user_dict[k])
        play_and_like_url = play_and_like_head + str(user_dict[k])

        video_info = get_user_info(video_url, fans_url, play_and_like_url)
        # print(len(video_info))

        info_to_db(video_info)



    # video_url = video_url_head + str(uid1)
    # fans_url = fans_url_head + str(uid1)
    # play_and_like_url = play_and_like_head + str(uid1)

    # userInfo6 = getUserAll("https://v.douyin.com/exKnyoG/")
    # videos_to_db(userInfo6)
