from agent import user_agent_list
from filedb import writeline
from bs4 import BeautifulSoup
import time
import random
import logging
import requests
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class Crawler:
    def __init__(self,_keyword,_page):
        self.session = requests.session()
        self.crawl_timestamp = int()
        self.keyword = _keyword
        self.page = _page

    def run(self):
        while True:
            self.crawler()
            time.sleep(10)
            if self.page > 500:
                break

    def crawler(self):
        while True:
            self.session.headers.update(
                {
                    'user-agent': random.choice(user_agent_list)
                }
            )
            url_str = 'https://link.springer.com/search/page/{}?facet-language=%22En%22&facet-content-type=%22Article%22&query={}'.format(self.page, self.keyword)
            try:
                r = self.session.get(url=url_str)
            except requests.exceptions.ChunkedEncodingError:
                print("Chunked!")
            soup = BeautifulSoup(r.content, 'lxml')
            target_tags = soup.find_all('a', attrs={'class': 'title'})
            href_list = []
            springer_headstr = 'https://link.springer.com/'
            for tag in target_tags:
                s = []
                for item in tag.stripped_strings:
                    s.append(item)
                title = ' '.join(s)
                title = re.sub('<[^<]+?>', '', title).strip()
                href_list.append((springer_headstr + tag['href'],title))
            for href,title in href_list:
                self.AbsCrawler(href,title)
            break
        logger.info('page {} Successfully crawled.'.format(self.page))
        self.page = self.page + 1


    def AbsCrawler(self,href,title):
        logger.info("crawling::: {} ::: at ::: {}".format(title,href))
        time.sleep(5)
        self.session.headers.update(
            {
                'user-agent': random.choice(user_agent_list)
            }
        )
        try:
            r = self.session.get(url=href)
        except requests.exceptions.ChunkedEncodingError:
            print("Chunked!")
        soup = BeautifulSoup(r.content, 'lxml')
        abs1_sec = soup.find('section', attrs={'aria-labelledby': "Abs1"})
        if abs1_sec:
            if abs1_sec.p:
                s = []
                for item in abs1_sec.p.stripped_strings:
                    s.append(item)
                items = ' '.join(s)
                item = re.sub('<[^<]+?>', '', items).strip()
                if isinstance(item, str):
                    line = title + '|'+ item
                    writeline(line)

if __name__ == '__main__':
    crawler = Crawler('data+mining',13)
    crawler.run()