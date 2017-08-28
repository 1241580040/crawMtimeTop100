# -*- coding: utf-8 -*-
import scrapy
import random
from crawMtimeTop100_.items import Crawmtimetop100Item
import re
from Carbon.Files import fHasBundle
import os

class MtimeSpider(scrapy.Spider):
    name = "mtime"
    allowed_domains = ["http://www.mtime.com"]
    start_urls = (
        'http://www.mtime.com/top/movie/top100',
    )

    def parse(self, response):
        top100To10Page = []
        top100To10Page.append(u"http://www.mtime.com/top/movie/top100")
        #获得page2-10,每页有十部电影
        webSites = response.xpath("//div[@id='PageNavigator'][@class='pagenav tc']/a/@href").extract()
        for webSite in webSites:
            top100To10Page.append(webSite)
        print "+"*80
        print top100To10Page
        print "+"*80

        for webSite in top100To10Page:
            request = scrapy.Request(webSite, callback=self.parse_page, dont_filter=True)
            yield request


    def parse_page(self, response):
        #print response
        #allpics = response.xpath("//script[@type='text/javascript']").extract()[4]

        allMovieWebsite = response.xpath("//div/ul[@id='asyncRatingRegion']/li//h2/a/@href").extract()
        print allMovieWebsite
        
        for oneMovieWebsite in allMovieWebsite:
            oneMovieAllPicWebSite = oneMovieWebsite+"posters_and_images/"
            print oneMovieAllPicWebSite
            request = scrapy.Request(oneMovieAllPicWebSite, callback=self.parse_item, dont_filter=True)
            print request
            yield request
        
    def parse_item(self, response):
        print "aaaa"
        allpics = response.xpath("//script[@type='text/javascript']").re('\"img_1000\":\"(.+?jpg)\"')
        #picName = response.xpath("//title").extract()[0]
        picName = response.xpath("/html/body/div[@id='db_sechead']/div[@class='db_head']/div[@class='clearfix']/h1/a").extract()[0]
        regexName = re.compile(">(.+?)<")
        picName = regexName.findall(picName)[0].encode("utf8")
        print picName
        picCount = len(allpics)
        print picCount
        
        moivePhotoUrlsPath = "./moviePhotoUrls"
        if os.path.exists(moivePhotoUrlsPath):
            pass
        else:
            os.makedirs(moivePhotoUrlsPath)
        with open(os.path.join(moivePhotoUrlsPath, picName+"_"+str(picCount)+".txt"), "w") as fh:
            for picWebSite in allpics:
                fh.write(picWebSite+"\n")
        
        i = 0
        for pic in allpics:
            i = i+1
            item = Crawmtimetop100Item()
            addr = pic 
            item['name'] = picName+"_"+str(i)
            item['picCount'] = picCount
            item['addr'] = addr
            print "+++++"+item['addr']
            print "+++++"+item['name']
            yield item
            
