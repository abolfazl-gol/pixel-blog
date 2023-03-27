from rest_framework import serializers
from .models import Posts, Comments
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    exclude = ('password',)

class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Posts
    fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comments
    fields = '__all__'
