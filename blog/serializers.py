from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    exclude = ('password',)

class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Image
    fields = '__all__'