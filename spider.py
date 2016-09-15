import requests
import json
import os
import gevent
import logging
from functools import partial
from lxml import html as xhtml
from pyquery import PyQuery as pq
from mongoengine import *  # noqa
import time

logger = logging.getLogger(__file__)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # noqa
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

SETTINGS = os.path.join(os.path.dirname(__file__), "spiders.json")

SCRAPY_PAGES = 50

connect('fun')  # noqa


class Post(Document):  # noqa
    # 标题
    title = StringField(required=True, unique=True)  # noqa
    # 发表日期
    post_time = DateTimeField(required=True)  # noqa
    # 内容
    content = StringField(required=True)  # noqa


class Spider:
    def __init__(self, *args, **kwargs):
        with open(SETTINGS, "r") as f:
            settings = json.load(f)[self.name]
            self.url = settings['url']
            self.proxies = settings.get('proxies')
            if self.proxies:
                self.req = partial(requests.get, proxies=self.proxies)
            else:
                self.req = partial(requests.get)

    def _parse_content(self, page, document):
        """解析内容，返回一个元组：(title, post_time, content)"""
        raise NotImplementedError

    def _parse_index(self, page):
        """解析首页"""
        raise NotImplementedError

    def _get_index_urls(self):
        raise NotImplementedError

    def parse_index(self):
        """返回首页列表，返回结果是一个列表，存放详细页面的url，比如：
        【http://www.fanjian.net/post/89762, http://www.fanjian.net/post/89763】
        """
        logger.info("开始爬取{}的首页".format(self.name))
        index_urls = self._get_index_urls()

        ret_urls = []

        def _parse(url):
            html = self.req(url).text
            page = xhtml.fromstring(html)
            ret_urls.extend(self._parse_index(page))

        threads = [gevent.spawn(_parse, url) for url in index_urls]
        gevent.joinall(threads)

        return ret_urls

    def parse_content(self, url):
        """解析内容页，将其存放到mongodb中"""
        logger.info("解析文章内容，地址为：{}".format(url))
        html = self.req(url).text
        page = xhtml.fromstring(html)
        document = pq(page)
        title, post_time, content = self._parse_content(page, document)
        post = Post(title=title, post_time=post_time, content=content)
        try:
            post.save()
        except Exception as e:
            logger.error(e)

    def run(self):
        start = time.time()
        # 内容页的url
        page_urls = self.parse_index()

        threads = [gevent.spawn(self.parse_content, url) for url in page_urls]
        gevent.joinall(threads)

        # for url in page_urls:
        #     self.parse_content(url)
        end = time.time()
        logger.info("爬取{}共花费时间为: {:.2f} s".format(self.name, end - start))
