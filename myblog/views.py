from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Blog, Category, Tag
# from pure_pagination import PageNotAnInteger, Paginator
from django.core.paginator import Paginator
import markdown
from comments.forms import CommentForm
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q


def blog_list(request):
    # 根据GET请求中查询条件
    # 返回不同排序的对象数组
    if request.GET.get('order') == 'views':
        blog_list = Blog.objects.all().order_by('-views')
        order = 'views'
    else:
        # 修改变量名称（articles -> article_list）
        blog_list = Blog.objects.all()
        order = 'normal'

    # 每页显示 1 篇文章
    paginator = Paginator(blog_list, 2)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    blog_list = paginator.get_page(page)

    context = {'blog_list': blog_list, 'order': order}
    return render(request, 'myblog/index.html', context)


'''    
class IndexView(ListView):
    """
    首页
    """
    model = Blog
    template_name = 'myblog/index.html'
    context_object_name = 'blog_list'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)

        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data
'''


class ArchiveView(ListView):
    model = Blog
    template_name = 'myblog/index.html'
    context_object_name = 'blog_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super().get_queryset().filter(create_time__year=year,
                                             create_time__month=month)


class TagView(ListView):
    model = Blog
    template_name = 'myblog/index.html'
    context_object_name = 'blog_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, id=self.kwargs.get('tag_id'))
        return super().get_queryset().filter(tag=tag)


class CategoryView(ListView):
    model = Blog
    template_name = 'myblog/index.html'
    context_object_name = 'blog_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, id=self.kwargs.get('category_id'))
        return super().get_queryset().filter(category=cate)


class BlogDetailView(DetailView):
    model = Blog
    tempate_name = 'myblog/blog_detail.html'
    context_object_name = 'blog'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        blog = super().get_object(queryset=queryset)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        blog.content = md.convert(blog.content)
        blog.toc = md.toc
        return blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "请输入关键词"
        return render(request, 'myblog/index.html', {'error_msg': error_msg})

    blog_list = Blog.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
    return render(request, 'myblog/index.html', {'error_msg': error_msg,
                                                 'blog_list': blog_list
                                                 })
