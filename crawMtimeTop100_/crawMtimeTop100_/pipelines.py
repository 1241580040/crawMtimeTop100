# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import urllib2
#import random
import requests
import time

class Crawmtimetop100Pipeline(object):
    def process_item(self, item, spider):
#         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}

        webHost = item['addr'].split("/")[2]
        #webBody = "/"+"/".join(item['addr'].split("/")[3:])
        print "1-> "+webHost
        #print "2-> "+webBody
        
        headers = {
                    #"(Request-Line)": "GET "+webBody+" HTTP/1.1",
                    "Host": webHost,
                    "User-Agent":    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:53.0) Gecko/20100101 Firefox/53.0',
                    #"Accept":    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept': '*/*',
                    "Accept-Language":   'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                    "Accept-Encoding":    'gzip, deflate',
                    
                    "Connection":    'keep-alive',
                    "Upgrade-Insecure-Requests": "1",          
                }
        
        print "cccc"
        #print host
#         req = urllib2.Request(url=item['addr'], headers=headers) #  
#         res = urllib2.urlopen(req)
        
        res = requests.get(item['addr'], headers=headers)
        
        #在这里可以判断下get的status, res.status,来判断请求是否有error，200正常，400badrequest/403 request forbidden
        
        #print res
        #print res.url
        #print res.headers
        #print res.content 二进制数据
        
        saveFilePath = os.path.join(os.path.curdir, "down_pic", item['name'].split("_")[0]+"_"+str(item["picCount"]))
        if os.path.exists(saveFilePath):
            pass
        else:
            #os.mkdir(saveFilePath) #只能建单层文件夹
            os.makedirs(saveFilePath)
        file_name = os.path.join(saveFilePath, item['name'] + '.jpg')
        with open(file_name, 'wb') as fp: #把二进制流存成jpg的文件
            fp.write(res.content)
        with open("./savePath.txt", "a") as fh: #查看生成的顺序
            fh.write(file_name+"\n")
        
        if os.path.getsize(file_name) < 3000: #抓取数据不全的URL会写到errorPic.txt中去
            with open("./errorPic.txt", "a") as fh:
                fh.write(item['addr']+"\n")
        else:
            pass
        
        print "-> sleep...1s..."
        time.sleep(1)
        
        
        
