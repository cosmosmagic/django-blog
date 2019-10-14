from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    org = models.CharField('用户名', max_length=128, blank=True)
    telephone = models.CharField('电话', max_length=50, blank=True)
    mod_date = models.DateTimeField('更新日期', auto_now=True)
    avatar=models.ImageField('头像',upload_to='avatar/%Y%m%d/', blank=True)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = '用户文档'
        verbose_name_plural = verbose_name
