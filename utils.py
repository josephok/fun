from functools import wraps
from pyquery import PyQuery


def pyquery_patch(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        fn = lambda: this.map(lambda i, el: PyQuery(this).outerHtml())  # noqa
        PyQuery.fn.listOuterHtml = fn
        return func(*args, **kwargs)
    return func_wrapper
