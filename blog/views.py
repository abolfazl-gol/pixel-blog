from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView, Response, status
from .models import  Posts, Comments, PostLikes
from server.authenticate import Authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError

class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Posts
    fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comments
    fields = '__all__'

class Authe(APIView):
  def __init__(self, ):
    self.SECRET_KEY = 'python_jwt'

  def post(self, request):
    data = request.data
    try:
      user = User.objects.create_user(username=data['username'],email=data['email'], password=data['password'])

      user = UserSerializer(user).data

      return Response({'status':status.HTTP_201_CREATED, 'data': user})
    except IntegrityError:
      return Response({"status": status.HTTP_409_CONFLICT, "error":"email already exists"})
    except Exception as err:
      print('error:', err)
      return Response(status=status.HTTP_400_BAD_REQUEST)


class Post(APIView):
  # permission_classes = (Authenticate,)
  def get(self, req):
    posts = Posts.objects.filter(author_id=1)
    posts = PostSerializer(posts, many=True).data

    return Response({'status': status.HTTP_200_OK, 'posts': posts})

  def post(self, req):
    print('user: ', req)
    data = req.data
    post = Posts.objects.create(author_id=1 ,title=data['title'], content=data['content'], subject=data['subject'], image=data['image'])
    post = PostSerializer(post).data

    return Response({'status': status.HTTP_201_CREATED, 'posts': post})


  def put(self, req, post_id=None):
    data = req.data
    if post_id is not None:
      try:
        post = Posts.objects.get(id=post_id)
        post.title = data['title']
        post.content = data['content']
        post.save()
        post = PostSerializer(post).data
        return Response({'status':status.HTTP_200_OK, 'post':post})
      except Posts.DoesNotExist:
        return Response({'status': status.HTTP_404_NOT_FOUND, 'error': 'post not found'})
      except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': str(err)})
    else:
      return Response(status=status.HTTP_400_BAD_REQUEST)
    
  
  def delete(self, req, post_id):
    if post_id is not None:
      try:
        Posts.objects.get(id=post_id).delete()
        return Response(status=status.HTTP_200_OK)
      except Posts.DoesNotExist:
        return Response({'status': status.HTTP_404_NOT_FOUND, 'error': 'post not found'})
      except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': str(err)})
    else:
      return Response(status=status.HTTP_400_BAD_REQUEST)
    
class Comment(APIView):
  def get(self, req, post_id=None):
    try:
      comments = Comments.objects.filter(post_id=post_id)
      comments = CommentSerializer(comments, many=True).data

      return Response({'status': status.HTTP_200_OK, 'comments': comments})
    except Comments.DoesNotExist:
      return Response({'status': status.HTTP_404_NOT_FOUND, 'error': 'post id not found'})
    except Exception as err:
      return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': str(err)})
  
  def post(self, req, post_id=None):
    Comments
    comment = Comments.objects.create(user_id= 1, post_id=post_id ,content=req.data['content'])
    comment = CommentSerializer(comment).data

    return Response({'status': status.HTTP_201_CREATED, 'comment': comment})
  
  def put(self, req, comment_id=None):
    if comment_id is not None:
      try:
        comment = Comments.objects.get(id=comment_id)
        comment.content = req.data['content']
        comment.save()
        comment = CommentSerializer(comment).data
        return Response({'status':status.HTTP_200_OK, 'comment':comment})
      except Comments.DoesNotExist:
        return Response({'status': status.HTTP_404_NOT_FOUND, 'error': 'comment not found'})
      except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': str(err)})
    else:
      return Response(status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self, req, comment_id):
    if comment_id is not None:
      try:
        Comments.objects.get(id=comment_id).delete()
        return Response(status=status.HTTP_200_OK)
      except Comments.DoesNotExist:
        return Response({'status': status.HTTP_404_NOT_FOUND, 'error': 'comment not found'})
      except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': str(err)})
    else:
      return Response(status=status.HTTP_400_BAD_REQUEST)
    

class PostLike(APIView):
  def post(self, req, post_id):
    # user_id = req.user
    post_like = PostLikes.objects.filter(post_id=post_id, user_id=1)
    print('len: ', len(post_like))
    if len(post_like) < 0:
      PostLikes.objects.create(post_id=post_id, user_id=1)
      return Response(status=status.HTTP_200_OK)
    else:
      PostLikes.objects.get(post_id=post_id, user_id=1).delete()
      return Response(status=status.HTTP_200_OK)