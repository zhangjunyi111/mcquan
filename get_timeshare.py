import scrapy


class GetTimeshareSpider(scrapy.Spider):
    name = "get_timeshare"
    allowed_domains = ["web.ifzq.gtimg.cn"]
    start_urls = ["https://web.ifzq.gtimg.cn"]

    def parse(self, response):
        pass
