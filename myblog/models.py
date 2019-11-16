from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import markdown
from django.utils.html import strip_tags


class Category(models.Model):
    """
    文章分类
    """
    name = models.CharField(verbose_name='文章类别', max_length=20)
    number = models.IntegerField(verbose_name='分类数目', default=1)

    class Meta:
        verbose_name = '文章类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    文章标签
    """
    name = models.CharField(verbose_name='文章标签', max_length=20)
    number = models.IntegerField(verbose_name='标签数目', default=1)

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Blog(models.Model):
    """
    博客
    """
    title = models.CharField(verbose_name='标题', max_length=100)
    content = models.TextField('正文', default='')
    create_time = models.DateTimeField('创建时间', default=timezone.now)
    modify_time = models.DateTimeField('修改时间', auto_now=True)
    click_nums = models.IntegerField('点击量', default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='文章类别')
    tag = models.ManyToManyField(Tag, verbose_name='文章标签')
    excerpt = models.CharField(verbose_name='文章摘要', max_length=200, blank=True, default='No Value')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    views = models.PositiveIntegerField(verbose_name='阅读量', default=0)
    avatar=models.ImageField(upload_to='article/%Y%m%d',blank=True,null=True)
    

    class Meta:
        ordering = ['-create_time', 'title']
        verbose_name = '我的博客'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('myblog:blog_detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.content))[:54]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Blog, self).save(*args, **kwargs)
