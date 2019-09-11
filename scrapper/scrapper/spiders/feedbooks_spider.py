import scrapy
from ..items import *


class GenericSpider(scrapy.Spider):
    name = "feedbooks"

    def start_requests(self):
        urls = [
            "http://es.feedbooks.com/books/top?category=FBFIC029000&lang=en"
            "http://es.feedbooks.com/books/top?category=FBFIC028000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBFIC002000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBFIC022000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBFIC009000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBFIC027000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBFIC015000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBFIC033000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBFIC014000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBFIC019000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBFIC016000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBFIC024000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBDRA000000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBFIC032000&lang=en",
            "http://es.feedbooks.com/books/top?category=FSHUM000000N&lang=en",
            "http://es.feedbooks.com/books/top?category=FBBIO000000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBHIS000000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBREL000000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBSOC000000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBSCI000000N&lang=en",
            "http://es.feedbooks.com/books/top?category=FBTRV000000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBART000000N&lang=en",
            "http://es.feedbooks.com/books/top?category=FBHUM000000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBLIT000000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBCOM000000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBBUS000000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBSACT000000&lang=en",
            "http://es.feedbooks.com/books/top?category=FBEDU000000&lang=en",
        ]

        for url in urls:
            print("New Url", url)
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_item(self, response):
        resp = response.xpath("//body").get()
        if resp is not None:
            # print(resp)
            yield TripleItem(subject=self.name, predicate="hasRaw", object=resp, source=response.url)

    def parse_list(self, response):
        resp = response.xpath("//h3/a/@href").getall()
        for item in resp:
            if item is not None:
                # print(item)
                yield response.follow(item, self.parse_item)
        next_page = response.xpath("//a[@class='next_page']/@href").get()
        if next_page is not None:
            # print("Next : ", next_page)
            yield response.follow(next_page, self.parse_list)

    # def parse(self, response):
    #     resp = response.xpath("//p[@class='facet']/a/@href").getall()
    #     print(resp)
    #     for item in resp:
    #         print("http://es.feedbooks.com" + item)
