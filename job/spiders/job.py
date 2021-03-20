import scrapy
import re
import time
from lxml import etree
from job.items import JobItem
from job.settings import creat_table


class job(scrapy.Spider):
    name = 'job'
    start_urls = ['https://www.58.com/changecity.html?catepath=job.shtml&catename=%E6%8B%9B%E8%81%98%E4%BF%A1%E6%81%AF&fullpath=9224&PGTID=0d202408-001f-4ff3-942f-bded66f03b13&ClickID=2']
    def parse(self,response):
        html = etree.HTML(response.text.replace('\n', ''))
        if0 = str(html.xpath('//script/text()'))[1:-1]
        ido = str(re.findall('"(.*?)":\{', if0)).split('}')
        ifo = []
        for i in ido[2:-2]:
            if i == ido[2]:
                idq = []
                ido[2] = i.replace('var cityList = {', ',')
                for t in ido[2].split(',')[2:-1]:
                    idq.append(re.findall('(.*)\|', t)[0][1:].strip())
                ifo.append(idq)
            else:
                idq = []
                for t in i.split(',')[2:]:
                    idq.append(re.findall('(.*)\|', t)[0][1:].strip())
                ifo.append(idq)
        for j in ifo:
            for i in j:
                city = re.findall('\w*',i)[-2]
                city2 = re.findall('(.*?)":', i)[0].replace('"','').replace("'",'').strip()
                print('city"=====','https://{}.58.com/job.shtml'.format(city))
                print(city,'=======',i,'========',city2)
                yield scrapy.Request('https://{}.58.com/job.shtml'.format(city),callback=self.parse1,meta={'city2':city2,'city':city})

    def parse1(self,response):
        item = JobItem()
        city = response.meta['city']
        city2 =response.meta['city2'] # 用于表格
        ul_list = response.xpath('//*[@id="sidebar-right"]/ul')
        sql = 'create table if not exists {} (title varchar(30) null,' \
              'price varchar(25) null,requie varchar(30) null,' \
              'company varchar(25) null)charset=utf8mb4;'.format(city2)
        creat_table(sql)
        print('CREAT TABLE SUSECESS')
        item['city_table'] = city2
        time.sleep(2)
        for ur in ul_list:
            li_list = ur.xpath('./li')
            for li in li_list:
                print('https://{}.58.com'.format(city)+li.xpath('./strong/a/@href').extract_first())
                yield scrapy.Request('https://{}.58.com'.format(city)+li.xpath('./strong/a/@href').extract_first(),callback=self.parse2,meta={'item': item})

    def parse2(self,response):
        print('目标网站：||||||||||||||||||||||', response.url,'\n','开始提取','\n')
        clear = response.xpath('//i[@class="total_page"]/text()')
        print(clear, '\n'*5)
        if clear == []:
            print(type(clear))
            print('对应连接没有内容，pass:\n',response.url)
            print('--------------------------------------------\n', response.text)
        else:
            item = response.meta['item']
            li_list = response.xpath('//*[@id="list_con"]/li')
            for li in li_list:
                item['price'] = li.xpath('./div[1]/p/text()').extract_first()
                item['title'] = li.xpath('./div[1]/div[1]/a/span[1]/text()').extract_first()+'|'+li.xpath('./div[1]/div[1]/a/span[2]/text()').extract_first()
                item['company'] = li.xpath('./div[2]/div/a/text()').extract_first()
                p_list = li.xpath('./div[2]/p/span')
                rquire = ''
                for p in p_list:
                    data = p.xpath('./text()').extract_first()
                    rquire = rquire+'|'+data
                item['requie'] = rquire
                print(item)
                yield item
            next_page = response.xpath('//a[@class="next"]/@href').extract_first()
            if next_page != None:
                print('下一页',next_page)
                yield scrapy.Request(next_page, callback=self.parse2,meta={'item': item})
            else:
                print('这个站点提取完成：\n 标志：',re.findall("next disabled", response.text))




