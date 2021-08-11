
import json

import os

import requests

from lxml import etree



headers = {
'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
'Accept': 'text/html',
'Cookie': "_uuid=1DBA4F96-2E63-8488-DC25-B8623EFF40E773841infoc; buvid3=FE0D3174-E871-4A3E-877C-A4ED86E20523155831infoc; LIVE_BUVID=AUTO8515670521735348; sid=l765gx48; DedeUserID=33717177; DedeUserID__ckMd5=be4de02fd64f0e56; SESSDATA=cf65a5e0%2C1569644183%2Cc4de7381; bili_jct=1e8cdbb5755b4ecd0346761a121650f5; CURRENT_FNVAL=16; stardustvideo=1; rpdid=|(umY))|ukl~0J'ulY~uJm)kJ; UM_distinctid=16ce0e51cf0abc-02da63c2df0b4b-5373e62-1fa400-16ce0e51cf18d8; stardustpgcv=0606; im_notify_type_33717177=0; finger=b3372c5f; CURRENT_QUALITY=112; bp_t_offset_33717177=300203628285382610"
}
resp = requests.get('https://www.bilibili.com/video/BV1Bh41127PZ',headers=headers)


def getBiliBiliVideo(url, p, bv):
    session = requests.session()

    res = session.get(url=url, headers=headers, verify=False)

    _element = etree.HTML(res.content)

    # 获取window.__playinfo__的json对象,[20:]表示截取'window.__playinfo__='后面的json字符串

    videoPlayInfo = str(_element.xpath('//head/script[5]/text()')[0].encode('utf-8').decode('utf-8'))[20:]

    videoJson = json.loads(videoPlayInfo)

    print(type(videoPlayInfo))
    print(videoPlayInfo)
    # print(resp.text)




if __name__ == '__main__':
    getBiliBiliVideo("https://www.bilibili.com/video/BV1Bh41127PZ", 3, "BV1Bh41127PZ")