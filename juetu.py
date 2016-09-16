import logging
from spider import Spider
from utils import pyquery_patch

logger = logging.getLogger(__name__)


class JuetuSpider(Spider):
    name = "掘图志"
    need_decode = True
    page_pattern = "page/"

    def _parse_index(self, page):
        return page.xpath("//div[@class='title-left']/h3/a/@href")

    @pyquery_patch
    def _parse_content(self, page, document):
        # 标题
        title = page.xpath("//div[@class='title-left']/h3/a/text()")[0]
        # 发布日期
        post_time = page.xpath("//div[@class='meta']/p/text()")[1]
        # 内容
        content = "".join(document(".box-left>p").listOuterHtml()[:-2])

        logger.info("解析{}的内容，标题为：{}".format(self.name, title))

        return (title, post_time, content)
