import time

from fanjian import FanjianSpider  # noqa
from juetu import JuetuSpider  # noqa
from qiqu import QiquSpider  # noqa
from wuliao import WuliaoSpider  # noqa
from multiprocessing import Pool
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

start = time.time()


def crawl(spider):
    spider().run()


# 运行Spider所有子类的爬虫，放到进程池中运行
spiders = Spider.__subclasses__()
pool = Pool()
pool.map(crawl, spiders)
# close the pool and wait for the work to finish
pool.close()
pool.join()

end = time.time()
logger.info('啦啦啦，{}个爬虫，总共花费{:.2f} s'.format(len(spiders), end - start))
