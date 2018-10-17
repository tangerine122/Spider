"""
@author:Adam
@time:2018-10-17 13:06
@desc:抓取花瓣100张美女图片
"""
import requests
import re
import json


def get_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/69.0.3497.100 Safari/537.36",
        # 如果抓取过多花瓣网可能要用户登录，这个加入cookies来模拟登录
    }
    r = requests.get(url, headers=headers)
    return r.text


def parse(html):
    # 正则解析
    result = re.findall('app.page\["pins"\] = (.*?);\napp.page\["ads"\]', html, re.S)[0]
    pins = json.loads(result)
    for pin in pins:
        pin_id = pin.get('pin_id')
        img_key = pin['file'].get('key')
        img_url = "http://img.hb.aicdn.com/" + img_key
        with open('{}.jpg'.format(pin_id), "wb+") as f:
            f.write(requests.get(url=img_url).content)
            print("{}下载完成".format(pin_id))
    return pin_id


if __name__ == "__main__":
    i = 1
    for _ in range(20):
        if i == 1:
            url = "http://huaban.com/favorite/beauty?jncoyxor&limit=5"
        else:
            url = "http://huaban.com/favorite/beauty?jncpiscw&max={}&limit=5&wfl=1".format(pin_id)
        html = get_url(url)
        pin_id = parse(html)
        i += 1
