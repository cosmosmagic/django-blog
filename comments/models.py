from django.db import models


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    blog = models.ForeignKey('myblog.Blog', on_delete=models.CASCADE)
    user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.user.username + self.text[:20]

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
