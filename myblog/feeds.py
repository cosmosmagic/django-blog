from django.contrib.syndication.views import Feed
from .models import Blog


class AllBlogsRssFeed(Feed):
    title = "Django博客"
    link = "/"
    description = "Django个人博客"

    def items(self):
        return Blog.objects.all()

    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    def item_description(self, item):
        return item.content
