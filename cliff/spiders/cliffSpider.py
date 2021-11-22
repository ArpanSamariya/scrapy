import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from cliff.items import CliffItem


class CliffSpider(Spider):
    # Initialising variables

    # product_category for Topwears, Will be changed to "footwear" for shoe
    category = "topwear"
    # Website to be scrapped, will be changed to shoe link later
    base = "http://www.net-a-porter.com/en-in/shop/clothing/tops?pageNumber={}"
    # Page Number to access subsequent pages of the link.
    page = 1
    # Name of spider
    name = "cliffSpider"
    allowed_domains = ["net-a-porter.com"]
    # Boolean to switch from topwear to footwear
    first_website = True
    # Scrapping starts from here with pageNumber = 1
    start_urls = [base.format(1)]

    # Default Callback Function
    def parse(self, response):
        # Get the div with class mentioned and grab anchor child
        products = Selector(response).xpath("//div[@class = 'ProductGrid52 ProductListWithLoadMore52__listingGrid']/a")

        # Iterate through each anchor element fetched above
        for product in products:
            # store data scrapped as per mentioned selector to corresponding field.
            item = CliffItem()
            item['name'] = product.xpath(".//div/div/div[2]/div/span/span[3]/text()").get()
            item['brand'] = product.xpath(".//div/div/div[2]/div/span/span[1]/text()").get()
            item['original_price'] = float(product.xpath(".//span[@class = 'PriceWithSchema9__value']/span/@content").get())
            item['sale_price'] = float(product.xpath(".//span[@class = 'PriceWithSchema9__value']/span/@content").get())
            item['image_url'] = product.xpath(".//div/div[1]/div/div[1]/div/div/div/picture/img/@src").get()
            item['product_page_url'] = product.xpath(".//@href").get()
            # assign product_category field of item with value of self.category
            item['product_category'] = self.category
            print(item)
            yield item

        # Increment to access next page
        self.page = self.page + 1

        if self.page < 26:
            next_page_url = self.base.format(self.page)
            # callback to scrap next url
            yield scrapy.Request(next_page_url)

        # Once all 25 Pages of Topwear have been scrapped
        # page is set to 1
        # base url is changed to shoe link
        # category is changed to "footwear"
        # setting first_website to false so that whenever next time page is 26,
        # it wont call same link
        if self.page == 26 and self.first_website:
            self.first_website = False
            self.page = 1
            self.base = "https://www.net-a-porter.com/en-in/shop/shoes?pageNumber={}"
            self.category = "footwear"
            next_page_url = self.base.format(self.page)
            yield scrapy.Request(next_page_url)


