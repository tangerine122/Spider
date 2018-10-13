"""
@author:Adam
@time:2018-10-12 9:09
@desc:抓取豆瓣top250数据
https://movie.douban.com/top250
"""
import requests
from lxml import etree
import re
from pymongo import MongoClient
import pymysql


def MovieUrl():
    # 创建空列表保存每个电影的url
    movieUrls = []
    url = "https://movie.douban.com/top250"
    # 页码循环
    for page in range(10):
        urlPage = "{}?start={}".format(url, page*25)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        }
        # 请求
        response = requests.get(url=urlPage, headers=headers)
        # 指定应答编码格式，按照服务器指定的编码解析
        response.encoding = response.apparent_encoding
        # 解析电影url
        html = etree.HTML(response.text)
        movieHref_list = html.xpath("//ol[@class='grid_view']/li/div[@class='item']/div[@class='pic']/a/@href")
        for movieHref in movieHref_list:
            movieUrls.append(movieHref)
    return movieUrls


def Movie(movieUrl):
    # 创建一个空字典保存电影信息
    movie = {}
    # 请求单个电影
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    }
    resMovie = requests.get(url=movieUrl, headers=headers)
    resMovie.encoding = "utf-8"
    htmlMovie = etree.HTML(resMovie.text)
    # 电影名
    title = htmlMovie.xpath("//div[@id='content']/h1/span[1]/text()")[0]
    movie["title"] = title
    # 平均评分
    vote_average = htmlMovie.xpath("//strong[@class='ll rating_num']/text()")[0]
    movie["vote_average"] = vote_average
    # 评价人数
    vote_count = htmlMovie.xpath("//a[@class='rating_people']/span/text()")[0]
    movie["vote_count"] = vote_count
    # 导演
    director = htmlMovie.xpath("//div[@id='info']/span[1]/span[@class='attrs']/a/text()")[0]
    movie["director"] = director
    content_str = htmlMovie.xpath("string(//div[@class='subject clearfix']/div[@id='info'])")
    # 主要演员
    try:
        casts_list = re.findall("主演: (.*?)\n", content_str, re.S)[0].strip().split(" / ")
        casts = "|".join(casts_list)
    except:
        casts = "无"
    movie["casts"] = casts
    # 类型
    genres_list = re.findall("类型: (.*?)\n", content_str, re.S)[0].strip().split(" / ")
    genres = "|".join(genres_list)
    movie["genres"] = genres
    # 制片国家
    district_list = re.findall("制片国家/地区: (.*?)\n", content_str, re.S)[0].strip().split(" / ")
    district = "|".join(district_list)
    movie["district"] = district
    # 语言
    language_list = re.findall("语言: (.*?)\n", content_str, re.S)[0].strip().split(" / ")
    language = "|".join(language_list)
    movie["language"] = language
    # 上映日期
    release_date_list = re.findall("上映日期: (.*?)\n", content_str, re.S)[0].strip().split(" / ")
    release_date = "|".join(release_date_list)
    movie["release_date"] = release_date
    # 片长
    runtime_list = re.findall("片长: (.*?)\n", content_str, re.S)[0].strip().split(" / ")
    runtime = "|".join(runtime_list)
    movie["runtime"] = runtime
    # IMDb编号
    imdbid = re.findall("IMDb链接: (.*?)\n", content_str, re.S)[0].strip()
    movie["imdbid"] = imdbid

    return movie


def Mongo(movie):
    # 存入MongoDB
    myconn = MongoClient("127.0.0.1", 27017)
    mydb = myconn["doubanmovie"]
    mycoll = mydb["top250"]
    mycoll.insert(movie)


def CreateTable(myconn, cursor):
    # 创建MySQL数据表
    create_table = """
            CREATE TABLE top250(
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(1000),
            vote_average VARCHAR(255),
            vote_count VARCHAR(255),
            director VARCHAR(255),
            casts VARCHAR(1000),
            genres VARCHAR(1000),
            runtime VARCHAR(1000),
            language VARCHAR(1000),
            release_date VARCHAR(1000),
            district VARCHAR(1000),
            imdbid VARCHAR(1000)
            );
            """
    cursor.execute(create_table)
    myconn.commit()


def InsertInto(myconn, cursor, movie):
    # MySQL存入数据
    insert_into = """
        INSERT INTO top250(title, vote_average, vote_count, director, casts, genres, runtime , language, release_date, district,imdbid) VALUES 
        ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}","{}");
        """.format(movie["title"], movie["vote_average"], movie["vote_count"], movie["director"], movie["casts"],
                   movie["genres"], movie["runtime"], movie["language"], movie["release_date"], movie["district"],
                   movie["imdbid"])
    cursor.execute(insert_into)
    myconn.commit()


def ConnSQL():
    # 连接MySQL
    global top
    host = input("请输入MySQL服务地址:")
    user = input("请输入MySQL用户：")
    password = input("请输入MySQL密码：")
    db = input("请输入MySQL要保存的数据库（请先保证该数据库已被创建）：")
    myconn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            charset='utf8'
    )
    cursor = myconn.cursor()
    return myconn, cursor


def MySQL(myconn, cursor, movie):
    # 存入MySQL
    global top
    if top == 1:
        CreateTable(myconn, cursor)
    InsertInto(myconn, cursor, movie)


if __name__ == "__main__":
    movieUrl_list = MovieUrl()
    top = 0
    myconn, cursor = ConnSQL()
    for movieUrl in movieUrl_list:
        top += 1
        print(top)
        movie = Movie(movieUrl)
        print(movie)
        # Mongo(movie)
        MySQL(myconn, cursor, movie)
    myconn.close()
