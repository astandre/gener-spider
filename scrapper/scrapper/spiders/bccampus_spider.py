import scrapy
from scrapy.selector import Selector
from ..items import *
from ..services import *


class GenericSpider(scrapy.Spider):
    name = "bccampus"
    # rules = [['//div[@class="row laText"]/div/h3/a/text()', "hasName"],
    #          ['//div[@class="row laText"]/div/div/div/a[1]/text()', "hasCreator"]]

    rules = None
    subject = None
    next = None
    urls = None
    carry_rule = None
    cont = 0

    def start_requests(self):
        urls = [
            "https://open.bccampus.ca/browse-our-collection/find-open-textbooks/"
        ]

        # data = init_spider("12345")
        # self.urls = data["urls"]
        self.subject = "open bccampus"
        # self.rules = data["rules"]
        # self.next = data["next"]

        # print(data)
        for url in urls:
            print("New Url", url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_follow(self, response):

        resp = response.xpath("//div[@class='col-md-9']").get()
        if resp is not None:
            yield TripleItem(subject=self.subject, predicate="hasRaw", object=resp)
            # self.carry_rule = None

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)

        # print(response.xpath('//b/@itemprop="name"'))
        # print(response.xpath('//b/@itemprop="name"').get())
        # for rule in self.rules:
        # contenidos = response.xpath('//div[@class="row laText"]').getall()
        # print("COntenidos")
        # values = []

        resp = response.xpath("//h4/a/@href").getall()
        if resp is not None:
            for next_page in resp:
                if next_page is not None:
                    yield response.follow(next_page, self.parse_follow)
            # yield TripleItem(subject=self.subject, predicate=rule["name"], object=resp_aux)

        # elif rule["type"] == "O":
        #     resp = response.xpath(rule["rule"]).get()
        #     if resp is not None:
        #         yield TripleItem(subject=self.subject, predicate=rule["name"], object=resp)
        #
        # elif rule["type"] == "X":
        #     # print(response.url)
        #     # print(rule["next"])
        #     self.carry_rule = rule["next"]
        #     next_page = response.xpath(rule["rule"]).getall()
        #     if next_page is not None:
        #         for page in next_page:
        #             print("Access  >>", page)
        #             yield response.follow(page, self.parse_follow)
        # yield scrapy.Request(url=response.url, callback=self.parse)
        # print(self.cont)
        pages = response.xpath("//section[@class='p-3']/p/a/@href").getall()
        if self.cont < len(pages):
            next_page = pages[self.cont]
            if next_page is not None:
                print("Next Page >>", next_page)
                self.cont += 1
                yield response.follow(next_page, self.parse)
