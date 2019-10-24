from scrapy import Spider, Request
from singlemalts.items import SinglemaltsItem

import re # needs to be imported here if used in shell
import math

class SingleMaltsSpider(Spider):
    name = 'singlemalts_spider'
    allowed_domains = ['www.masterofmalt.com']
    # get the 500 most popular ones
    start_urls = ['https://www.masterofmalt.com/country-style/scotch/single-malt-whisky/']
    #start_urls = ['https://www.masterofmalt.com/country-style/scotch/single-malt-whisky/name/']
    # # request to start_urls what do we do parse

    def parse(self, response):
        # get numbers of whiskies per page class="col-md-12"
        id_info = response.xpath('//*[@id="productBoxWideContainer"]//div[@class = "boxBgr product-box-wide h-gutter js-product-box-wide"]/@id').extract()
        num_per_page = len(id_info)
        total_pages = math.ceil(500/num_per_page) # hardcoded number, get the 500 most popular scotch whiskies!
    # find result_urls
        result_urls = ["https://www.masterofmalt.com/country-style/scotch/single-malt-whisky/name/{}/".format(x) for x in range(1, total_pages+1)]

#       if

        for url in result_urls[:1]: # limit right now to first 2
            yield Request(url= url, callback = self.parse_result_page)
        # this is a scrapy request, which method to use to parse

    def parse_result_page(self, response):
        product_urls = response.xpath('//*[@id="productBoxWideContainer"]//div[@class = "boxBgr product-box-wide h-gutter js-product-box-wide"]/@data-product-url').extract()
        print(len(product_urls))
        print('=' * 50)

#        price_paths = response.xpath('//*[@id="ContentPlaceHolder1_ctl00_pricesWrapper"]')

#       try:
#           price = resp
#       except:
#           price = ""


        for url in product_urls:
                yield Request(url= url, callback = self.parse_product_page)
                # obtain Whisky details (Country, Region, Distillery, Age) from box

    def parse_product_page(self, response):

#        try:
#            number_of_reviews = response.xpath('//*[@id="ContentPlaceHolder1_productRating_productUserRating"]/a/div[2]/text()').extract()
#           review_nr = re.findall(r'\d+', number_of_reviews)
#        except:
#            number_of_reviews = ''

        try:
            name = response.xpath('//*[@id="ContentPlaceHolder1_pageH1"]/text()').extract()
        except:
            name = ''

        try:
            region = response.xpath('//*[@id="ContentPlaceHolder1_ctl00_ctl00_wdRegion"]/span[2]/a/text()').extract()
        except:
            region = ''

        try:
            distillery = response.xpath('//*[@id="ContentPlaceHolder1_ctl00_ctl00_wdDistillery"]/span[2]/a/text()').extract()
        except:
            distillery = ''

        try:
            age = response.xpath('//*[@id="ContentPlaceHolder1_ctl00_ctl00_wdYearsMatured"]/span[2]/a/text()').extract()
        except:
            age = ''

        try:
            # obtain Whisky tasting notes By the Chaps at Master of Malt
            tasting_notes = response.xpath('//*[@id="ContentPlaceHolder1_ctl00_ctl02_TastingNoteBox_ctl00_breakDownTastingNote"]//p/text()').extract()
        except:
            tasting_notes = ''

        # price not on this page

        try:
            rating = response.xpath('//*[@id="ContentPlaceHolder1_productRating_productUserRating"]/a/div[1]/meta[3]/@content').extract()
        except:
            rating = ''


        item = SinglemaltsItem()
        item['name'] = name
        item['region'] = region
        item['distillery'] = distillery
        item['age'] = age
        item['tasting_notes'] = tasting_notes
        item['rating'] = rating
#        item['review_nr'] = review_nr
        #item['price'] = price

        yield item
