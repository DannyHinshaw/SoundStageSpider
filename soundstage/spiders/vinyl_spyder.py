import scrapy
from time import sleep
from pprint import pprint
from scrapy.loader import ItemLoader
from soundstage.items import Vinyl

class VinylSpider(scrapy.Spider):

    name = "vinyl_spider"

    def __init__(self, category=None, *args, **kwargs):
        super(VinylSpider, self).__init__(*args, **kwargs)
        self.base = 'http://www.soundstagedirect.com/'
        self.start_url = self.base + 'artistIndex.php'
        self.start_urls = [self.start_url]

    def parse(self, response):

        # artist name letter page links (containing artists by name)
        links = response.xpath('//*[@id="colleft"]/div/a/@href').extract()

        # include start_url in list to be passed
        links.insert(0, self.start_url)

        for link in links:
            # parse each alpha index page
            yield scrapy.Request(link, callback=self.parse_index_page)

    def parse_index_page(self, response):

        # links to artist pages (containing artist albums)
        artist_links = response.xpath('//*[@id="colmain"]/ul/li/a/@href').extract()

        for artist in artist_links:

            # not likely any artist hasa more than 96 albums, so it is set as max
            link = self.base + artist + '?limit=96'

            # build artist page request
            # grab the current letter in sort
            request = scrapy.Request(link, callback=self.parse_artist_page)
            request.meta['vinyl_alpha'] = response.xpath('//div[@class="index"]/strong/text()').extract()

            # 'return' while testing. 'yield' production
            yield request

    def parse_artist_page(self, response):

        # links to album detail pages
        album_links = response.xpath('//*[@id="category-products"]/ul/li/h2/a/@href').extract()

        for album in album_links:

            # build album page request
            # get current letter in sort from passed meta-data
            request = scrapy.Request(album, callback=self.parse_album_page)
            request.meta['vinyl_alpha'] = response.meta['vinyl_alpha']
            yield request

    def parse_album_page(self, response):

        # create instance of VinylItem for each vinyl
        l = ItemLoader(item=Vinyl(), response=response)

        # load all collected item fields
        l.add_value('vinyl_alpha', response.meta['vinyl_alpha'])
        l.add_value('vinyl_url', response.url)
        l.add_xpath('vinyl_sku', 'normalize-space(.//*[@id="sku"]/text())')
        l.add_xpath('vinyl_upc', 'normalize-space(.//*[@id="product"]/div[4]/dl/dd[5]/text())')
        l.add_xpath('vinyl_name', 'normalize-space(.//*[@id="product"]/div[2]/h1/text())')
        l.add_xpath('vinyl_genre', 'normalize-space(.//*[@id="product"]/div[4]/dl/dd[3]/text())')
        l.add_xpath('vinyl_price', 'normalize-space(.//span[@class="newprice"]/text())')
        l.add_xpath('vinyl_price', 'normalize-space(.//div[@class="price"]/text())')
        l.add_xpath('vinyl_artist_name', 'normalize-space(.//*[@id="product"]/div[2]/p/a/text())')
        l.add_xpath('vinyl_description', 'normalize-space(.//*[@id="product"]/div[4]/dl/dd[4]/text())')
        return l.load_item()
