import scrapy
from ..items import BettyandbiddyItem

class BettyandbiddySpider(scrapy.Spider):
    name = "summer_sale"
    page_number = 2
    start_urls = [
        "https://bettyandbiddy.com/collections/summer-sale?page=1"
    ]

    def parse(self, response):
        items = BettyandbiddyItem()
        all_products = response.css(".on-sale")

        for product in all_products:
            product_name = product.css(".boost-pfs-filter-product-item-title::text").extract_first()
            product_original_price = product.css("s .money::text").extract_first()
            product_sale_price = product.css(".boost-pfs-filter-product-item-sale-price .money::text").extract_first()
            product_imagelink = product.css(".lazyloaded , .on-sale:nth-child(17) .boost-pfs-filter-product-item-image-link::attr(src)").extract_first()

            items["product_name"] = product_name
            items["product_original_price"] = product_original_price
            items["product_sale_price"] = product_sale_price
            items["product_imagelink"] = product_imagelink

            yield items


        next_page = "https://bettyandbiddy.com/collections/summer-sale?page=" + str(BettyandbiddySpider.page_number)
        if BettyandbiddySpider.page_number < 6:
            BettyandbiddySpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)