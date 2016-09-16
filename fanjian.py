import logging
from spider import Spider

logger = logging.getLogger(__name__)


class FanjianSpider(Spider):
    name = "犯贱志"
    page_pattern = "latest-"

    def _parse_index(self, page):
        return page.xpath("//h2[@class='cont-list-title']/a/@href")

    def _parse_content(self, page, document):
        # 标题
        title = page.xpath("//h1/@title")[0]
        # 发布日期
        post_time = page.xpath("//div[contains(@class, 'view-info')]/text()",
            namespaces={"re": r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}'})[1].strip()
        # 内容
        content = document(".view-main").html()

        logger.info("解析{}的内容，标题为：{}".format(self.name, title))

        return (title, post_time, content)
