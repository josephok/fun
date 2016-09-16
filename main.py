from fanjian import FanjianSpider  # noqa
from juetu import JuetuSpider  # noqa
from qiqu import QiquSpider  # noqa
from multiprocessing.dummy import Pool as ThreadPool
from spider import Spider

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
    spider().run()


# 运行Spider所有子类的爬虫，放到线程池中运行
spiders = Spider.__subclasses__()
pool = ThreadPool()
pool.map(crawl, spiders)
# close the pool and wait for the work to finish
pool.close()
pool.join()
