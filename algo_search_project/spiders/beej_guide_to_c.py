from pathlib import Path
from datetime import datetime
import scrapy
import json

class BeejGuideToCSpider(scrapy.Spider):
    name = "beej_guide_to_c"
    allowed_domains = ["beej.us"] # change to 
    start_urls = ["https://beej.us/guide/bgc/html/split/foreword.html"]
    # file:///home/benjamin/coding/algo-search/algo_search_project/site.html
    # https://beej.us/guide/bgc/html/split/foreword.html
    def parse(self, response):
        page_title_formatted = response.css("h1::text").get()
        page_title_snake_case = response.css("h1::attr(id)").get()
        parsed_text_array = (response.xpath("//body//text()").getall())
        parsed_text_trimmed = parsed_text_array[6:-5]
        final_text = [item for item in parsed_text_trimmed if item != '\n']
        final_text = ' '.join(final_text)

        data_obj = {
                'page_title': page_title_formatted,
                'url': response.url,
                'body': final_text
                }
        data_json = json.dumps(data_obj, ensure_ascii=False) 
       
        with open('beej-upload', 'a') as file:
            file.write('{ "index": { "_index": "sites" } }\n')
            file.write(f'{data_json}\n')

        # filename = f'beej-{page_title_snake_case}.html'
        # Path(f'./beej-guide-to-c/{filename}').write_text(parsed_text_trimmed)
        next_page = response.css('div[style="text-align:center"] a:last-of-type::attr(href)').getall()[-1]
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

