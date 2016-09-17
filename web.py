import tornado.ioloop
import tornado.web
import json
import os
from tornado.options import define, options
from spider import Post
from datetime import datetime

# 每页显示数量
ITEMS_PER_PAGE = 10
# 分页栏的数目
TOTAL_PAGES_IN_VIEW = 10

define("port", default=80, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class PostHandler(tornado.web.RequestHandler):
    def get(self):
        # 解析页数
        page = self.get_query_argument("p")
        # 解析查询关键字，只支持title搜索
        try:
            query = self.get_query_argument("q")
        except tornado.web.MissingArgumentError:
            query = None
        offset = (int(page) - 1) * ITEMS_PER_PAGE
        if query:
            q_posts = Post.objects(title__icontains=query)
        else:
            q_posts = Post.objects
        posts = q_posts.order_by('-post_time').skip(offset).limit(
            ITEMS_PER_PAGE)
        # 总共页数
        total_pages_in_db = len(q_posts) / ITEMS_PER_PAGE
        if total_pages_in_db != len(q_posts) // ITEMS_PER_PAGE:
            total_pages_in_db += 1
        total_pages_in_db = int(total_pages_in_db)
        if total_pages_in_db < TOTAL_PAGES_IN_VIEW:
            total_pages = total_pages_in_db
        else:
            total_pages = TOTAL_PAGES_IN_VIEW

        ret_posts = {
            'total_pages_inview': total_pages,
            'posts': [],
            'last_page': total_pages_in_db
        }
        for post in posts:
            title = post.title
            post_id = str(post.id)
            ret_posts['posts'].append({'title': title, 'id': post_id})
        self.write(json.dumps(ret_posts))


class DetailHandler(tornado.web.RequestHandler):
    def get(self, post_id):
        post = Post.objects.get(id=post_id)

        ret_post = {
            'title': post.title,
            'post_time': datetime.strftime(post.post_time, "%Y-%m-%d %H:%M"),
            'content': post.content,
            'id': str(post.id)
        }

        self.write(json.dumps(ret_post))

    def delete(self, _id):
        # 删除某个post
        passcode = self.request.headers.get('passcode')
        if passcode and passcode == "6YeH5qGR5a2Q":
            Post.objects(id=_id).delete()
        else:
            self.set_status(401)


def make_app():
    handlers = [
        (r"/api/posts/", PostHandler),
        (r"/api/posts/(\w{24})", DetailHandler),
        (r"/", IndexHandler)
    ]
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    return tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(options.port, address='127.0.0.1')
    tornado.ioloop.IOLoop.current().start()
