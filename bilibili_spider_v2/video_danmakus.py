#示例：获取视频弹幕

from bilibili_api import video, sync, user
import pandas as pd
from bilibili_api.video import *
from bilibili_api.user import *
import jieba
from wordcloud import WordCloud,ImageColorGenerator,random_color_func
import matplotlib.pyplot as plt

v = video.Video(bvid='BV1gC4y1h722')
# vc = video.Video(bvid='BV1gC4y1h722')
u = user.User.get_up_stat(309947633)


dms = sync(v.get_danmakus(0))

dataframe = pd.DataFrame(columns=['bullet_screen'])

for i, dm in enumerate(dms):

    # print(i, dm.text)
    # df = dataframe.append({'bullet_screen': dm.text}, ignore_index=True)
    dataframe.loc[i] = dm.text
print(dataframe)

dataframe.to_csv("video_bullet_screen_1.csv",index=False, encoding='utf-8-sig')

# print(len(dms))

# wc = WordCloud(
#     background_color='white',
#     color_func=random_color_func,
#     random_state=50,
# )

# def add_word(list):
#     for items in list:
#         jieba.add_word(items)

# add_word(my_words_list)

# word_cloud = wc.generate(dataframe)
# word_cloud.to_file("rm.jpg")

# plt.imshow(word_cloud)
# plt.axis('off')
# plt.show()





