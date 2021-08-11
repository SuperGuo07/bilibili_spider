#示例：获取用户粉丝数

from bilibili_api import user, sync

u = user.User(660303135)

print(sync(u.get_relation_info())["follower"])