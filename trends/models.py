from django.db import models
from posts.models import Post

# Create your models here.

class Trend(models.Model):
    keyword = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    search_volume = models.IntegerField()
    started_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.keyword