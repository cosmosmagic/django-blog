from django.db.models.aggregates import Count
from ..models import Blog, Category, Tag
from django import template

register = template.Library()


@register.simple_tag
def get_recent_blogs(num=5):
    return Blog.objects.all().order_by('-create_time')[:num]


@register.simple_tag
def archives():
    return Blog.objects.dates('create_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_blogs=Count('blog')).filter(num_blogs__gt=0)


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_blogs=Count('blog')).filter(num_blogs__gt=0)
