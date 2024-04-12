from bs4 import BeautifulSoup
from math import floor
import scrapy
import json
import time

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

        index_obj = {
                'index': { 
                          '_index': 'sites',
                          '_id': response.url
                          }
        }
        index_json = json.dumps(index_obj, ensure_ascii=False) 

        [title, chapter_title, body]= extract_text(response.text) 
        data_obj = {
                'title_element': title,
                'chapter_title': chapter_title,
                'url': response.url,
                'body': body,
                'time': int(time.time())
                }
        data_json = json.dumps(data_obj, ensure_ascii=False) 
       
        with open(f'{self.prefix}_{floor(self.url_count / 10)}', 'a') as file:
            file.write(f'{index_json}\n')
            file.write(f'{data_json}\n')
        self.url_count += 1

# source: https://stackoverflow.com/questions/1936466/how-to-scrape-only-visible-webpage-text-with-beautifulsoup/73701993#73701993
def extract_text(html):
    soup = BeautifulSoup(html, "lxml")
  
    # ignore reportOptionalMemberAccess warning
    title = soup.title.text
    try:
        chapter_title = soup.title.text
    except AttributeError:
        chapter_title = "untitled"

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
