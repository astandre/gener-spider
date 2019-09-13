import scrapy
from ..items import *


class GenericSpider(scrapy.Spider):
    name = "opentextbooks"

    subject = "Open textBooks"

    def start_requests(self):
        urls = [
            "https://open.umn.edu/opentextbooks/subjects/accounting-finance"
            "https://open.umn.edu/opentextbooks/subjects/business",
            "https://open.umn.edu/opentextbooks/subjects/human-resources",
            "https://open.umn.edu/opentextbooks/subjects/management",
            "https://open.umn.edu/opentextbooks/subjects/marketing",
            "https://open.umn.edu/opentextbooks/subjects/computer-science-information-systems",
            "https://open.umn.edu/opentextbooks/subjects/economics",
            "https://open.umn.edu/opentextbooks/subjects/education",
            "https://open.umn.edu/opentextbooks/subjects/humanities"
            "https://open.umn.edu/opentextbooks/subjects/engineering",
            "https://open.umn.edu/opentextbooks/subjects/arts",
            "https://open.umn.edu/opentextbooks/subjects/history",
            "https://open.umn.edu/opentextbooks/subjects/languages",
            "https://open.umn.edu/opentextbooks/subjects/linguistics"
            "https://open.umn.edu/opentextbooks/subjects/literature-rhetoric-and-poetry",
            "https://open.umn.edu/opentextbooks/subjects/philosophy",
            "https://open.umn.edu/opentextbooks/subjects/journalism-media-studies-communications",
            "https://open.umn.edu/opentextbooks/subjects/law",
            "https://open.umn.edu/opentextbooks/subjects/mathematics",
            "https://open.umn.edu/opentextbooks/subjects/applied",
            "https://open.umn.edu/opentextbooks/subjects/pure",
            "https://open.umn.edu/opentextbooks/subjects/medicine",
            "https://open.umn.edu/opentextbooks/subjects/natural-sciences",
            "https://open.umn.edu/opentextbooks/subjects/biology",
            "https://open.umn.edu/opentextbooks/subjects/chemistry",
            "https://open.umn.edu/opentextbooks/subjects/physics",
            "https://open.umn.edu/opentextbooks/subjects/social-sciences",
            "https://open.umn.edu/opentextbooks/subjects/psychology",
            "https://open.umn.edu/opentextbooks/subjects/sociology",
            "https://open.umn.edu/opentextbooks/subjects/student-success"
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
