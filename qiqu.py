import logging
import re
from spider import Spider, SCRAPY_PAGES
from utils import pyquery_patch

logger = logging.getLogger(__name__)


class QiquSpider(Spider):
    name = "奇趣发现"
    need_decode = True

    def _get_index_urls(self):
        urls = [self.url]
        next_urls = ['{}catalog.asp?page={}'.format(self.url, i)
            for i in range(2, SCRAPY_PAGES + 1)]
        urls.extend(next_urls)
        return urls

    def _parse_index(self, page):
        return page.xpath("//h3/a/@href")

    @pyquery_patch
    def _parse_content(self, page, document):
        # 标题
        title = page.xpath("//h3/text()")[0]
        # 发布日期
        post_time = page.xpath("//div[@class='wz112']//td/text()")[-1]
        post_time = re.findall(r'\d{4}-\d+-\d+', post_time)[0]
        # 内容
        content = document(".align_entry_hack").html()
        doc = document(content)
        content = "".join(doc("p").listOuterHtml())

        logger.info("解析{}的内容，标题为：{}".format(self.name, title))
        return (title, post_time, content)
