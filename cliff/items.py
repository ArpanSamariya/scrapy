from scrapy.item import Item, Field

# Model Class to store data
class CliffItem(Item):
    name = Field()
    brand = Field()
    original_price = Field()
    sale_price = Field()
    image_url = Field()
    product_page_url = Field()
    product_category = Field()