import time
import requests
from fontTools.ttLib import TTFont
from lxml import etree
import re
from handle_db import handle_get_task

def handle_douyin_web_share(task):
    font = TTFont('DY.woff')
    font.saveXML('font2.xml')
    #提取font.xml中的cmap节点
    best_map = font['cmap'].getBestCmap()
    #进制发生了改变
    new_best_map = {}
    for key, value in best_map.items():
        new_best_map[hex(key)] = value
    #print(new_best_map)
    #构建网站上的字典
    new_map = {
        'x': '',
        'num_': '1',
        'num_1': '0',
        'num_2': '3',
        'num_3': '2',
        'num_4': '4',
        'num_5': '5',
        'num_6': '6',
        'num_7': '9',
        'num_8': '7',
        'num_9': '8',
    }
    new_data = {}
    for k, v in new_best_map.items():
        new_data[k] = new_map[v]
    #把new_data中的key值的0替换为&#
    rs = {}
    for k, v in new_data.items():
        rs['&#' + k[1:] + ';'] = v
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    url = 'https://www.iesdouyin.com/share/user/%s'%task['share_id']
    temp = requests.get(url=url, headers=headers)
    req = temp.text
    for k, v in rs.items():
        if k in req:
            req = req.replace(k, v)
    share_web_html = etree.HTML(req)
    #数据字典
    user_info = {}
    user_info['nickname'] = share_web_html.xpath("//p[@class='nickname']/text()")[0]
    douyin_id1 = share_web_html.xpath("//p[@class='shortid']/text()")[0].replace(' ','')
    douyin_id2 = ''.join(share_web_html.xpath("////p[@class='shortid']/i/text()")).replace(' ','')
    search_douyin_str = re.compile(r'抖音ID：')
    user_info['douyin_id'] = re.sub(search_douyin_str,'',douyin_id1 + douyin_id2)
    user_info['job'] = share_web_html.xpath("//span[@class='info']/text()")[0].replace(' ','')
    user_info['describe'] = share_web_html.xpath("//p[@class='signature']/text()")[0]
    user_info['guanzhu'] = ''.join(share_web_html.xpath("//p[@class='follow-info']/span[1]//i/text()")).replace(' ','')
    fans = ''.join(share_web_html.xpath("//p[@class='follow-info']/span[2]//i/text()")).replace(' ','')
    danwei1 = share_web_html.xpath("//p[@class='follow-info']/span[2]/span[1]/text()")[-1]
    if danwei1.strip() == 'w':
        user_info['fans'] = str(int(fans)/10) + 'w'
    like = ''.join(share_web_html.xpath("//p[@class='follow-info']/span[3]//i/text()")).replace(' ','')
    danwei2 = share_web_html.xpath("//p[@class='follow-info']/span[3]/span[1]/text()")[-1]
    if danwei2.strip() == 'w':
        user_info['like'] = str(int(like) / 10) + 'w'
    print(user_info)

if __name__ == '__main__':
    while True:
        task = handle_get_task()
        handle_douyin_web_share(task)
        time.sleep(1)


