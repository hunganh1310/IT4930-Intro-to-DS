import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['https://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.css('div.quote'):
            # Trích xuất thông tin cơ bản
            text = quote.css('span.text::text').get()
            author = quote.css('small.author::text').get()
            tags = quote.css('div.tags a.tag::text').getall()
            author_url = quote.css('small.author ~ a::attr(href)').get()

            # Gửi yêu cầu đến trang tác giả, truyền kèm thông tin quote
            yield response.follow(
                author_url,
                callback=self.parse_author,
                meta={'text': text, 'author': author, 'tags': tags}
            )

        # Crawl trang tiếp theo nếu có
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        # Nhận dữ liệu quote từ meta
        text = response.meta['text']
        author = response.meta['author']
        tags = response.meta['tags']

        # Trích xuất ngày sinh và nơi sinh
        born_date = response.css('span.author-born-date::text').get()
        born_location = response.css('span.author-born-location::text').get()

        yield {
            'text': text,
            'author': author,
            'tags': tags,
            'born_date': born_date,
            'born_location': born_location
        }
