import logging
from spider import Spider

logger = logging.getLogger(__name__)


class WuliaoSpider(Spider):
    name = "无聊图"
    page_pattern = "page/"

    def _parse_index(self, page):
        return page.xpath("//h1[@class='title']/a/@href")

    def _parse_content(self, page, document):
        # 标题
        title = page.xpath("//h1[@class='title']/text()")[0]
        # 发布日期
        post_time = page.xpath("//div[@class='details']/text()")[2].strip(
            "\r\n\t").strip()
        # 内容
        content = document("div.post>p").outer_html()
        logger.info("解析{}的内容，标题为：{}".format(self.name, title))

        return (title, post_time, content)
