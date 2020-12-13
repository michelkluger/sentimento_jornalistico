import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import pandas as pd


class FolhaSpider(CrawlSpider):
    name = "folha"
    start_urls = ["https://www1.folha.uol.com.br/ultimas-noticias/"]
    useful_links = []

    data_collected = pd.DataFrame()

    rules = [
        Rule(LinkExtractor(allow=".shtml"), callback="get_links",
             follow=False),
    ]

    def __find_date(self, lista):

        for item in lista:
            if " às " in item:
                print(item)

    def get_links(self, response):
        replace_dict = {
            "\n": "",
            "\t": "",
            "Assinantes podem liberar 5 acessos por dia para conteúdos da Folha":
            "",
            "Gostaria de receber as principais notícias": "",
            " do Brasil e do mundo?": "",
        }
        title = str(response).split("/")[-1].replace(".shtml>",
                                                     "").replace("-", " ")
        paragraphs = response.xpath('//*//p/text()').extract()
        date = response.xpath('//*/time').extract()
        self.__find_date(date)
        print(title)

        # print(date)
        return
        text = ''.join(paragraphs)
        for key, value in replace_dict.items():
            text = text.replace(key, value)
        # editor = Editado por Fábio Zanini (interino),
        print(text)

        # paragraph = paragraph[0:last_item]
        # print(paragraph)

        # def get_paragraphs(self, response):
        # //*[@id="conteudo"]/div[3]/p[5]/text()


import logging

logging.getLogger('scrapy').propagate = False

from scrapy.crawler import CrawlerProcess
c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0',
    # save in file CSV, JSON or XML
    'FEED_FORMAT': 'csv',  # csv, json, xml
    'FEED_URI': 'output.csv',  #
})
c.crawl(FolhaSpider, LOG_ENABLED=False)
c.start()
