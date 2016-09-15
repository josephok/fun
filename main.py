from fanjian import FanjianSpider
from juetu import JuetuSpider

from threading import Thread


def crawl(spider):
    spider.run()


spiders = (FanjianSpider(), JuetuSpider())

threads = []
for spider in spiders:
    t = Thread(target=crawl, args=(spider,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
