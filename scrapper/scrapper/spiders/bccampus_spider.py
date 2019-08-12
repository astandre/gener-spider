import scrapy
from scrapy.selector import Selector
from ..items import *
from ..services import *


class GenericSpider(scrapy.Spider):
    name = "bccampus"

    subject = "open bccampus"
    cont = 0

    def start_requests(self):
        urls = [
            "https://open.bccampus.ca/browse-our-collection/find-open-textbooks/"
        ]

        for url in urls:
            print("New Url", url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_follow(self, response):

        resp = response.xpath("//div[@class='col-md-9']").get()
        if resp is not None:
            yield TripleItem(subject=self.subject, predicate="hasRaw", object=resp)
            # self.carry_rule = None

    def parse(self, response):

        resp = response.xpath("//h4/a/@href").getall()
        if resp is not None:
            for next_page in resp:
                if next_page is not None:
                    yield response.follow(next_page, self.parse_follow)
        pages = response.xpath("//section[@class='p-3']/p/a/@href").getall()
        if self.cont < len(pages):
            next_page = pages[self.cont]
            if next_page is not None:
                print("Next Page >>", next_page)
                self.cont += 1
                yield response.follow(next_page, self.parse)
