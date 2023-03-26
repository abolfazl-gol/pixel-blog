from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Posts(models.Model):
  title = models.CharField(max_length=255)
  content = models.TextField()
  subject = models.CharField(max_length=255)
  image = models.ImageField()
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.title


class Comments(models.Model):
  content = models.TextField()
  vote_post = models.IntegerField(default=0)
  post = models.ForeignKey(Posts, db_column='post_id', on_delete=models.CASCADE)
  user = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.content


class PostLikes(models.Model):
  user_id = models.IntegerField()
  post_id = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    unique_together = ('user_id', 'post_id')