from spider import Spider, SCRAPY_PAGES


class FanjianSpider(Spider):
    name = "犯贱志"

    def _get_index_urls(self):
        urls = [self.url]
        next_urls = ['{}latest-{}'.format(self.url, i)
            for i in range(2, SCRAPY_PAGES + 1)]
        urls.extend(next_urls)
        return urls

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

        return (title, post_time, content)
