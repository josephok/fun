import logging
from spider import Spider, SCRAPY_PAGES
from pyquery import PyQuery

logger = logging.getLogger(__name__)


class JuetuSpider(Spider):
    name = "掘图志"
    need_decode = True

    def _get_index_urls(self):
        urls = [self.url]
        next_urls = ['{}page/{}'.format(self.url, i)
            for i in range(2, SCRAPY_PAGES + 1)]
        urls.extend(next_urls)
        return urls

    def _parse_index(self, page):
        return page.xpath("//div[@class='title-left']/h3/a/@href")

    def _parse_content(self, page, document):
        # 标题
        title = page.xpath("//div[@class='title-left']/h3/a/text()")[0]
        # 发布日期
        post_time = page.xpath("//div[@class='meta']/p/text()")[1]
        # 内容
        fn = lambda: this.map(lambda i, el: PyQuery(this).outerHtml())  # noqa
        PyQuery.fn.listOuterHtml = fn
        content = "".join(document(".box-left>p").listOuterHtml()[:-2])

        logger.info("解析{}的内容，标题为：{}".format(self.name, title))

        return (title, post_time, content)
