from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
from math import floor
import scrapy
import json
import csv
import re

class GenericSpider(scrapy.Spider):

    custom_settings = {
        "DEPTH_LIMIT": 0

    }

    def __init__(self, urls=None, prefix='page', *args, **kwargs):
        super(GenericSpider, self).__init__(*args, **kwargs)
        if urls is None:
            raise ValueError(
                    "No urls argument provided.\nuse -a {path to new line-seperated file of urls}"
                    )
        with open(f'{urls}', 'r') as file:
            self.start_urls = [line.rstrip() for line in file]
        self.prefix = prefix

    name = "generic_text_grab"
    url_count = 0
    def parse(self, response):
        [title, chapter_title, body]= extract_text(response.text) 
        data_obj = {
                'title_element': title,
                'chapter_title': chapter_title,
                'url': response.url,
                'body': body
                }
        data_json = json.dumps(data_obj, ensure_ascii=False) 
       
        # with open(f'pages/page_{floor(self.url_count / 10)}', 'a') as file:
        with open(f'{self.prefix}_{floor(self.url_count / 10)}', 'a') as file:
            file.write('{ "index": { "_index": "sites" } }\n')
            file.write(f'{data_json}\n')
        self.url_count += 1
        # filename = f'beej-{page_title_snake_case}.html'
        # Path(f'./beej-guide-to-c/{filename}').write_text(parsed_text_trimmed)
        # next_page = response.css('div[style="text-align:center"] a:last-of-type::attr(href)').getall()[-1]
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

# source: https://stackoverflow.com/questions/1936466/how-to-scrape-only-visible-webpage-text-with-beautifulsoup/73701993#73701993
def extract_text(html):
    soup = BeautifulSoup(html, "lxml")
  
    # ignore reportOptionalMemberAccess warning
    title = soup.title.text
    chapter_title = soup.h1.text
    # kill all script and style elements
    # need to remove math elements?
    for script in soup(['style', 'script', '[document]', 'head', 'object', 'link', 'template', 'math', 'footer']):
        script.decompose()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = ' '.join(chunk for chunk in chunks if chunk)

    return [title, chapter_title, text]
