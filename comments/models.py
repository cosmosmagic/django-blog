from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    blog = models.ForeignKey('myblog.Blog', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.user.username + self.text[:20]

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
