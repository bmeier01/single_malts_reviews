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

    def parse(self, response):
        # get numbers of whiskies per page class="col-md-12"
        id_info = response.xpath('//*[@id="productBoxWideContainer"]//div[@class = "boxBgr product-box-wide h-gutter js-product-box-wide"]/@id').extract()
        num_per_page = len(id_info)
        total_pages = math.ceil(800/num_per_page) # hardcoded number, get the 600 most popular scotch whiskies!

        # find result_urls
        result_urls = ["https://www.masterofmalt.com/country-style/scotch/single-malt-whisky/{}/".format(x) for x in range(1, total_pages+1)]

        # identify all product pages but only scrape those that have reviews
#        specifier = []
#        for i in range(0,len(id_info)):
#            specifier.append(re.findall(r'\d+', id_info[i])[1])
#        rating_paths = []
#        for i in range(0,len(specifier)):
#            rating_paths.append(response.xpath('//*[@id="ContentPlaceHolder1_ctl{}_containerRating"]'.format(specifier[i])).extract())
#
#        products_with_rating = [elem !=[] for elem in rating_paths]
#
#        all_product_urls = response.xpath('//*[@id="productBoxWideContainer"]//div[@class = "boxBgr product-box-wide h-gutter js-product-box-wide"]/@data-product-url').extract()
#        print(len(all_product_urls))
#        print('=' * 50)

        # take product_urls only of those for which rating_paths is not empty
        #def filter_by_rating (lis1, lis2):
#        product_urls = []
#        for idx in range(0,len(products_with_rating)):
#            if products_with_rating[idx]:
#                product_urls.append(all_product_urls[idx])

        # this is a scrapy request, which method to use to parse
#         product_urls = all_product_urls[list(map(lambda item: item!=[], rating_paths))]

        #product_urls = filter_by_rating(products_with_rating, all_product_urls)

#        products_with_rating = [elem !=[] for elem in rating_paths]
#        product_urls = list({key:value for (key,value) in dict(zip(products_with_rating, all_product_urls)).items() if value == True}.keys())
#
#        product_urls = []
#        if item in rating_paths !=[]:
#            product_urls.append(all_product_urls[index(item)])


#       try:
#           price_paths = response.xpath('//*[@id="ContentPlaceHolder1_ctl00_pricesWrapper"]//span/text()').extract()
#            price = re.findall(r'\$\d+\.\d+', ''.join(price))
#       except:
#           price = ""
        for url in result_urls[:1]: # limit right now to first 2
            yield Request(url= url, callback = self.parse_result_page)

    def parse_result_page(self, response):

        product_urls = response.xpath('//*[@id="productBoxWideContainer"]//div[@class = "boxBgr product-box-wide h-gutter js-product-box-wide"]/@data-product-url').extract()

        for url in product_urls:
            yield Request(url= url, callback = self.parse_product_page)
                

    def parse_product_page(self, response):
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
        #item['price'] = price

        yield item
