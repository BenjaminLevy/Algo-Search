from pathlib import Path
from datetime import datetime
from math import floor
import scrapy
import json
import csv
class GenericSpider(scrapy.Spider):

    custom_settings = {
        "DEPTH_LIMIT": 0

    }
    name = "generic_text_grab"
    url_count = 0
    start_urls = []
    with open('/home/benjamin/coding/algo-search/algo_search_project/books-to-scrape/links-to-scrape.txt', 'r') as file:
        start_urls = [line.rstrip() for line in file]
    def parse(self, response):
        chapter_title_formatted = response.css("h1::text").get()
        response.xpath("//script").remove() # remove JavaScript that would otherwise be picked up
        parsed_text_array = (response.xpath("//body//text()").getall())
        final_text = [item for item in parsed_text_array if item != '\n']
        final_text = ' '.join(final_text)

        data_obj = {
                'title_element': response.css('title::text').get(),
                'chapter_title': chapter_title_formatted,
                'url': response.url,
                'body': final_text
                }
        data_json = json.dumps(data_obj, ensure_ascii=False) 
       
        with open(f'pages/page_{floor(self.url_count / 10)}', 'a') as file:
        
            file.write('{ "index": { "_index": "sites" } }\n')
            file.write(f'{data_json}\n')
        self.url_count += 1
        # filename = f'beej-{page_title_snake_case}.html'
        # Path(f'./beej-guide-to-c/{filename}').write_text(parsed_text_trimmed)
        # next_page = response.css('div[style="text-align:center"] a:last-of-type::attr(href)').getall()[-1]
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

