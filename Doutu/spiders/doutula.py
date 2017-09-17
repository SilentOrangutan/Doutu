#coding=utf-8
import scrapy
from Doutu.items import DoutuItem
import os
import requests
#防止ascii编码错误
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Doutu(scrapy.Spider):  # 默认的回调parse方法
    name = 'doutu'
    allowed_domains = ['doutula.com']  # 定义域名范围
    #列表推导式 创建前N页url列表
    start_urls = ['http://www.doutula.com/photo/list/?page={}'.format(i) for i in range(1,2)]

    def parse(self, response):
        i=0
        for content in response.xpath('//*[@id="pic-detail"]/div/div[1]/div[2]/ul/li/div/div/a'):
            items = DoutuItem()
            i+=1
            # print(content.xpath('//img/@data-original').extract()[i])
            try:
                items['img_url']=content.xpath('//img/@data-original').extract()[i]
                # print(items['img_url'])
                items['name']=content.xpath('//p/text()').extract()[i]
                # print items['img_url']
            except Exception as e:
                raise IndexError

            try:
                filename='downloads/{}'.format(items['name'])+items["img_url"][-4:]
                if not os.path.exists(filename):
                    r=requests.get('http:'+items['img_url'])
                    with open(filename,'wb') as f:
                        f.write(r.content)
                print('tupiancunzai')
            except Exception as e:
                print(e,'-----')

            yield items
