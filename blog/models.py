from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
  title = models.CharField(max_length=255)
  content = models.TextField()
  subject = models.CharField(max_length=255)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'posts'

  def __str__(self):
    return self.title


class Comment(models.Model):
  content = models.TextField()
  vote_post = models.IntegerField(default=0)
  post = models.ForeignKey(Post, db_column='post_id', on_delete=models.CASCADE)
  user = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'comments'

  def __str__(self):
    return self.content


class PostLike(models.Model):
  user_id = models.IntegerField()
  post_id = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'post_likes'
    unique_together = ('user_id', 'post_id')

class Image(models.Model):
  image = models.ImageField(upload_to='images')
  post = models.ForeignKey(Post, db_column='post_id', on_delete=models.CASCADE)

  class Meta:
    db_table = 'images'

  def __str__(self):
    return self.title