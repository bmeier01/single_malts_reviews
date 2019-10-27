from scrapy import Spider, Request
from singlemalts.items import SinglemaltsItem

# import use packages
import re
import math

class SingleMaltsSpider(Spider):
    name = 'singlemalts_spider'
    allowed_domains = ['www.masterofmalt.com']
    # get the 750 most popular ones
    start_urls = ['https://www.masterofmalt.com/country-style/scotch/single-malt-whisky/']


    def parse(self, response):
        # get numbers of whiskies per page class="col-md-12"
        id_info = response.xpath('//*[@id="productBoxWideContainer"]//div[@class = "boxBgr product-box-wide h-gutter js-product-box-wide"]/@id').extract()
        num_per_page = len(id_info)
        total_pages = math.ceil(800/num_per_page) # hardcoded number. going through all may not be useful for customer, many very specialised and unique!

        # retrieve result_urls
        result_urls = ["https://www.masterofmalt.com/country-style/scotch/single-malt-whisky/{}/".format(x) for x in range(1, total_pages+1)]

        for url in result_urls[:30]: # limit to 750 most popular whiskies
            yield Request(url= url, callback = self.parse_result_page)

    def parse_result_page(self, response):
        # retrieve result_urls
        product_urls = response.xpath('//*[@id="productBoxWideContainer"]//div[@class = "boxBgr product-box-wide h-gutter js-product-box-wide"]/@data-product-url').extract()

        id_info = response.xpath('//*[@id="productBoxWideContainer"]//div[@class = "boxBgr product-box-wide h-gutter js-product-box-wide"]/@id').extract()
        specifier = []
        for i in range(0,len(id_info)):
            specifier.append(re.findall(r'\d+', id_info[i])[1])

        # get prices from first page
        price_links = []
        for i in specifier:
            price_links.append('//*[@id="ContentPlaceHolder1_ctl{}_pricesWrapper"]'.format(specifier[int(i)]))

        price = []
        for link in price_links:
            try:
                price_extract = response.xpath(link).extract()
                price_extract = re.findall(r'\$\d+\.\d+', ''.join(price_extract))
            except:
                price_extract = ""
            price.append(price_extract)

        #product_urls = response.xpath('//*[@id="productBoxWideContainer"]//div[@class = "boxBgr product-box-wide h-gutter js-product-box-wide"]/@data-product-url').extract()

        # pass price for each product with product url
        for i in range(len(product_urls)):
            yield Request(url= product_urls[i], meta={'price':price[i]}, callback = self.parse_product_page)

    def parse_product_page(self, response):

        price = response.meta['price']

        # obtain Whisky details (review numbers, rating, region, distillery, age, tasting notes)
        try:
            number_of_reviews = response.xpath('//*[@id="ContentPlaceHolder1_productRating_productUserRating"]/a/div[2]/text()').extract()
            number_of_reviews = re.findall(r'\d+', ''.join(number_of_reviews))
        except:
            number_of_reviews = ''

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
            age = re.findall(r'\d+', ''.join(age))
        except:
            age = ''

        try:
            # obtain Whisky tasting notes By the Chaps at Master of Malt
            tasting_notes = response.xpath('//*[@id="ContentPlaceHolder1_ctl00_ctl02_TastingNoteBox_ctl00_breakDownTastingNote"]//p/text()').extract()
        except:
            tasting_notes = ''

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
        item['number_of_reviews'] = number_of_reviews
        item['price'] = price

        yield item
