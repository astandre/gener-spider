import scrapy
from ..items import *

domain = 'https://florida.theorangegrove.org/'


class GenericSpider(scrapy.Spider):
    name = "orangegrove"

    subject = "Orange Groove"

    def start_requests(self):
        urls = [
            'https://florida.theorangegrove.org/og/hierarchy.do?topic=612a768f-4979-aa54-68ec-09affba54d09',
            'https://florida.theorangegrove.org/og/hierarchy.do?topic=acedc05e-0d93-f56d-0034-a70d3546f5e0',
            'https://florida.theorangegrove.org/og/hierarchy.do?topic=e17ea474-21cd-d407-9165-bbbc165884b4',
            'https://florida.theorangegrove.org/og/hierarchy.do?topic=0fd16144-0047-7064-ab78-1169c0cd3683',
            'https://florida.theorangegrove.org/og/hierarchy.do?topic=94c81979-5a4a-0e4c-f678-458e8d4aa9b8',
            'https://florida.theorangegrove.org/og/hierarchy.do?topic=b1530c9e-c5d9-cf13-e5f9-2a6391a2b163',
        ]

        for url in urls:
            print("New Url", url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_follow(self, response):

        resp = response.xpath("//div[@id='maincontent']").get()
        if resp is not None:
            yield TripleItem(subject=self.name, predicate="hasRaw", object=resp, source=response.url)

    def parse(self, response):
        resp = response.xpath("//a[contains(text(),'READ MORE')]/@href").getall()
        if resp is not None:
            for next_page in resp:
                if next_page is not None:
                    yield response.follow(next_page, self.parse_follow)
        next_page = response.xpath("//a[@rel='next'][1]/@href").get()
        print("Next Page >>", next_page)
        if next_page is not None:
            yield response.follow(next_page, self.parse)
