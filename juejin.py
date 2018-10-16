"""
@author:Adam
@time:2018-10-15 20:10
@desc:掘金小册抓取
"""
import requests
import json
for page in range(1, 3):
    url = "https://xiaoce-timeline-api-ms.juejin.im/v1/getListByLastTime?uid=&client_id=&token=&src=web&alias=&pageNum={}".format(page)
    header = {
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/69.0.3497.100 Safari/537.36"
    }
    r = requests.get(url, headers=header)
    content = json.loads(r.text)
    for d in content["d"]:
        title = d["title"]
        print(title)
        author = d["userData"]["username"]
        print("作者：{}".format(author))
        price = d["price"]
        print(price)
        buyCount = d["buyCount"]
        print("{}人已购买".format(buyCount))
        contentSize = d["contentSize"]
        print("字数：{}".format(contentSize))
        lastSectionCount = d["lastSectionCount"]
        print("{}小节".format(lastSectionCount))
        desc = d["desc"]
        print("简介：{}".format(desc))

        print("="*70)
