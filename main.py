from fanjian import FanjianSpider
from juetu import JuetuSpider
from threading import Thread

import logging

# disable requests info log.
logging.getLogger("requests").setLevel(logging.WARNING)
logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # noqa
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)


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
