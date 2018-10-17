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
        "Cookie": "_uab_collina=153819945925847380875843; "
                  "UM_distinctid=16623d51797ebf-025ecf2f5f9fe4-8383268-1fa400-16623d517984b5; "
                  "__auc=bc4bcc2816623d51952ed8276ab; "
                  "_umdata=ED82BDCEC1AA6EB902192A885B4B67644CD04CD48E6631C31E2540DB76E811E36CFFFC"
                  "9D70416D23CD43AD3E795C914C3E8A0C71A0B389DB679E459767E6679B; "
                  "sid=xMaklIkPih9ZlDAlp9Par6HWhxt.bvBlPt7w%2BurXYdFsytCK%2FyFmyWrBno92TEAkp%2BlbScQ; "
                  "_f=iVBORw0KGgoAAAANSUhEUgAAADIAAAAUCAYAAADPym6aAAABJElEQVRYR%2B1VOxYCIQwMF7KzsvFGXmW"
                  "9kY2VnQfxCvgCRmfzCD9lnz53myWQAJOZBEfeeyIi7xz%2FyEXzZRPFhYbPc3hHXO6I6TbFixmfEyByeQQSxu"
                  "6BcAXSkIGMazMjuBcz8pQcq44o0Iuyyc1p38C62kNsOdeSZDOQlLRQ80uOMalDgWCGMfsW2B5%2FATMUyGh2u"
                  "hgptV9Ly6l5nNOa1%2F6zmjTqkH2aGEk2jY72%2B5k%2BNd9lBfLMh8GIP11iK95vw8uv7RQr4oNxOfbQ%2F7"
                  "g5Z4meveyt0uKDEIiMLRC4jrG1%2FjkwKxCRE2e5lF30leyXYvQ628MZKV3q64HUFvnPAMkVuSWlEouLSiuV6"
                  "dp2WtPBrPZ7uO5I18tbXWvEC27t%2BTcv%2Bx0JuJAoUm2L%2FQAAAABJRU5ErkJggg%3D%3D%2CWin32.1920"
                  ".1080.24; __asc=1ef0ba811668065ade877f82b14; _trs_uv=jncow7wp_1245_ej9j; _ga=GA1.2.8459"
                  "1140.1539752520; _gid=GA1.2.662013574.1539752520; Hm_lvt_e9fe99c2267a6f7a9215a8724ce995"
                  "b4=1539752520; Hm_lpvt_e9fe99c2267a6f7a9215a8724ce995b4=1539752520; referer=https%3A%2F"
                  "%2Fwww.baidu.com%2Flink%3Furl%3Dt_557PSwSjgIatbXv4umb5ZQACN-2yW7fH2fKmNyQ4qgJ9f0MbOic6P"
                  "SwbOHLrjJ%26wd%3D%26eqid%3D81c3c16f000253c3000000025bc6c2a0; Hm_lvt_d4a0e7c3cd16eb58a654"
                  "72f40e7ee543=1539672086,1539752439,1539752615,1539752677; Hm_lpvt_d4a0e7c3cd16eb58a65472"
                  "f40e7ee543=1539753720; _cnzz_CV1256903590=is-logon%7Clogged-out%7C1539753721116; CNZZDAT"
                  "A1256903590=350008814-1538195526-%7C1539748284"

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
