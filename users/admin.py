from django.contrib import admin
from django.contrib.auth.models import User

from .models import UserProfile


# 定义一个行内 admin
class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'


# 将 Profile 关联到 User 中
class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]


# 重新注册 User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
