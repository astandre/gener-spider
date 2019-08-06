import scrapy
from scrapy.selector import Selector
from ..items import *
from ..services import *


class GenericSpider(scrapy.Spider):
    name = "train"
    # rules = [['//div[@class="row laText"]/div/h3/a/text()', "hasName"],
    #          ['//div[@class="row laText"]/div/div/div/a[1]/text()', "hasCreator"]]

    rules = None
    subject = None
    next = None
    urls = None
    carry_rule = None

    def start_requests(self):
        # urls = [
        #     'https://espanol.free-ebooks.net/categoria/arte-musica-teatro',
        # ]

        data = init_spider("12345")
        self.urls = data["urls"]
        self.subject = data["name"]
        self.rules = data["rules"]
        self.next = data["next"]

        print(data)
        for url in self.urls:
            print("New Url", url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_follow(self, response):
        print("NExt")
        print(self.carry_rule)
        print(response.url)
        if self.carry_rule is not None:
            resp = response.xpath(self.carry_rule["rule"]).get()
            print(resp)
            if resp is not None:
                yield TripleItem(subject=self.subject, predicate=self.carry_rule["name"], object=resp)
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

        for rule in self.rules:
            if rule["type"] == "A":
                resp = response.xpath(rule["rule"]).getall()
                if resp is not None:
                    for resp_aux in resp:
                        if resp_aux is not None:
                            yield TripleItem(subject=self.subject, predicate=rule["name"], object=resp_aux)
            elif rule["type"] == "O":
                resp = response.xpath(rule["rule"]).get()
                if resp is not None:
                    yield TripleItem(subject=self.subject, predicate=rule["name"], object=resp)

            elif rule["type"] == "X":
                # print(response.url)
                # print(rule["next"])
                self.carry_rule = rule["next"]
                next_page = response.xpath(rule["rule"]).getall()
                if next_page is not None:
                    for page in next_page:
                        print("Access  >>", page)
                        yield response.follow(page, self.parse_follow)
            # yield scrapy.Request(url=response.url, callback=self.parse)

        if self.next is not None:
            next_page = response.xpath(self.next).get()
            # print(next_page)
            print("Next Page >>", next_page)
            if next_page is not None:
                yield response.follow(next_page, self.parse)
