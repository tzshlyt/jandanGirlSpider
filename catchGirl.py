#!/usr/bin/ python
# _*_ coding: utf-8 _*_
import os
import urllib
import urllib2
import time
import random
import re

# 获取网页
def url_open(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36')

    # proxy_support = urllib2.ProxyHandler({"http": "182.89.6.104:8123"})
    # opener = urllib2.build_opener(proxy_support)
    # urllib2.install_opener(opener)

    try:
        response = urllib2.urlopen(req, timeout=30)

        html = response.read()
        return html
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason
            return None


# 取得当前起始页码
def get_page(url):
    html = url_open(url)
    pattern = re.compile('<span class="current-comment-page">\[(.*?)\]</span>', re.S)
    item = re.search(pattern, html)
    if item:
        return item.group(1)
    else:
        print 'why not get page'
        exit(-1)

# 获取图像地址
def find_imges(page_url):
    html = url_open(page_url)
    pattern = re.compile('<p>.*?<a href="(.*?)".*?</p>')
    items = re.findall(pattern, html)
    return items

# 保存图像
def save_images(folder, img_addrs):
    for each in img_addrs:
        time.sleep(random.uniform(1, 2))
        print "====downing..." + str(each)
        filname = each.split('/')[-1]
        with open(filname, 'wb') as file:
            img = url_open(each)
            file.write(img)
    pass

# 主程序
def download_mm(folder = "OOXX", pages = 3):

    # 判断文件夹是否存在
    isExists = os.path.exists(folder)
    if not isExists:
        os.mkdir(folder)
    os.chdir("OOXX")

    url = "http://jandan.net/ooxx"
    
    # 取得当前起始页码
    pag_num = int(get_page(url))
    
    for i in range(pages):
        pag_num -= i
        if pag_num < 1500:
            return

        # 爬取的网页
        page_url = url + "/page-" + str(pag_num) + "#comments"
        print "====pagUrl===" + page_url
        
        # 取得 图像 地址
        img_addrs = find_imges(page_url)

        # 保存图片到文件夹中
        save_images(folder, img_addrs)

        # 延时，防止服务器拒绝访问
        time.sleep(random.uniform(2, 4))

if __name__ == "__main__":
    download_mm("OOXX", 418)