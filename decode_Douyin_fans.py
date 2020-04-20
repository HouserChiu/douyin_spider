import json
from handle_db import save_task
#必须的格式
def response(flow):
    #通过Fiddler抓取接口
    if 'aweme/v1/user/follower/list' in flow.request.url:
        #数据解析
        for user in json.loads(flow.response.text)['followers']:
            douyin_info = {}
            douyin_info['share_id'] = user['uid']
            douyin_info['douyin_id'] = user['short_id']
            douyin_info['nickname'] = user['nickname']
            save_task(douyin_info)
