# -*- coding: utf-8 -*-
import requests
import json
from lxml import etree
# from multiprocessing.dummy import Pool as ThreadPool
import time
import sqlalchemy



# JsonDataDtc = []
def Get_Url(url):
    myPage = requests.get(url).content.decode("gbk")
    return myPage


#
# def Save_info(save_path, filename,slist):  # 写文件操作
#     if not os.path.exists(save_path):
#         os.makedirs(save_path)
#     path = save_path + "/" + filename + ".txt"
#     with open(path, "w+") as fp:
#             # fp.write(slist.encode("utf8"))
#             for s in slist:
#                 fp.write(s.encode("utf8"))


def Load_Json_Data(slist):  # 单线程应用
    for x in slist:
        Data = x.replace("data_callback(", "")
        jsonData = Data.replace(")", "")
        JsonDataDtc = json.loads(jsonData)
        Spider_News_Content(JsonDataDtc)

#
# def Load_Json_Data(slist):  # 多线程应用函数，处理json数据
#     # for x in slist:
#     Data = slist.replace("data_callback(", "")
#     jsonData = Data.replace(")", "")
#     JsonDataDtc = json.loads(jsonData)
#     Spider_News_Content(JsonDataDtc)


def Spider_News_Content(listdata):  # 爬虫主函数
    for u in listdata:
        # print u['title'] ,   u['docurl'],   u['time']
        ContentPage = Get_Url(u['docurl'])
        # print ContentPage
        Selector = etree.HTML(ContentPage)
        Title = Selector.xpath('//*[@id="epContentLeft"]/h1/text()')  # 正文标题
        for i in Title:
            print i
        FromAndTime = Selector.xpath('//*[@id="epContentLeft"]/div[1]/text()[1]')  # 时间
        for a in FromAndTime:
            print a[13:32]
        FromText = Selector.xpath('//*[@id="ne_article_source"]/text()')  # 新闻来源
        for c in FromText:
            print c
        FromUrl = Selector.xpath('//*[@id="ne_article_source"]/@href')  # 来源网址
        for b in FromUrl:
            print b
        Content = Selector.xpath('//*[@id="endText"]/p/text()')  # 正文
        for n in Content:
            print n
        author = Selector.xpath('//*[@id="endText"]/div[2]/span[2]/text()')  # 作者
        for v in author:
            print v
            print "========================================================================================================="



if __name__ == '__main__':
    Page = []
    start_url = "http://temp.163.com/special/00804KVA/cm_guoji.js?callback=data_callback"
    Page1 = Get_Url(start_url)
    Page.append(Page1)

    i = 2
    while i:
        Second_url = "http://temp.163.com/special/00804KVA/cm_guoji_0" + bytes(i) + ".js?callback=data_callback"
        Page2 = Get_Url(Second_url)
        if Page2.find('data_callback') == -1:
            break
        Page.append(Page2)
        i += 1

    time1 = time.time()  #
    Load_Json_Data(Page)
    # Spider_News_Content(JsonDataDtc)
    time2 = time.time()
    print u"单线程" + str(time2 - time1)

    # pool = ThreadPool(4)  # 多线程
    # time3 = time.time()
    # Results = pool.map(Load_Json_Data, Page)
    # pool.close()
    # pool.join()
    # time4 = time.time()
    # print u"多线程" + str(time4 - time3)
