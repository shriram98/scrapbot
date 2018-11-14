# -*- coding: utf-8 -*-
import scrapy


class RalphbotSpider(scrapy.Spider):
    name = 'ralphbot'
    allowed_domains = ['www.ralphlauren.com']
    start_urls = ['http://www.ralphlauren.com/']

    # This method gets each link from the navbar and sends each link to parse_page
    def parse(self, response):
        sub_link  = response.css('a[data-cgid]::attr(href)').extract()
        for page in sub_link :
            yield scrapy.Request(url=page, callback=self.parse_page, dont_filter=True)    

    # This method iterates over each item in the current page and scrapes the result to a csv file
    # parse_page goes to the next item page from the current page automatically
    def parse_page(self, response):           
        brand_name = response.css('div.product-tile div.brand-name::text').extract()
        product_name = response.css('.product-tile .product-name .name-link::text').extract()
        price = response.css('.product-tile .product-pricing .product-sales-price::text').extract()
        img_link = response.css('.product-tile .product-image .thumb-link img.default-img ::attr(src)').extract()

        for item in zip(brand_name, product_name, price, img_link):
            scraped_info = {
                'brand_name' : item[0],
                'product_name' : item[1],
                'price' : item[2],
                'img_link' : item[3],
            }

            yield scraped_info
        
        next_page = response.css('li.first-lastbar a::attr(href)').extract_first()
        if next_page is not None:
            # urljoin is used to load the next page
            next_page = response.urljoin(next_page) 
            yield scrapy.Request(url=next_page, callback=self.parse_page, dont_filter=True)
   
