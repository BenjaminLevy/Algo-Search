from pathlib import Path
import scrapy


class BeejGuideToCSpider(scrapy.Spider):
    name = "beej_guide_to_c"
    allowed_domains = ["beej.us"] # change to 
    start_urls = ["https://beej.us/guide/bgc/html/split/foreword.html"]
    #response.xpath("//body//text()")
    def parse(self, response):
        raw_page_title = response.css("h1::attr(id)").get()
        formatted_page_title = ' '.join(word.capitalize() for word in raw_page_title.split('-'))
        # page = response.css("title::text").extract()
        # parsed_text_array = (response.xpath("//body//text()").getall())
        # parsed_text_trimmed = parsed_text_array[6:-5]

        with open('beej-index-and-titles-test.txt', 'a') as file:
            file.write(f'{formatted_page_title}\n')
        #filename = f'beej-{page_title}.html'
        #Path(f'./beej-guide-to-c/{filename}').write_text(parsed_text_trimmed)
        next_page = response.css('div[style="text-align:center"] a:last-of-type::attr(href)').getall()[-1]
        # print('....................................')
        # print()
        # print('...................................')
        if next_page is not None:
            with open('beej-index-and-titles-test.txt', 'a') as file:
                file.write(f'{next_page}...')
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

