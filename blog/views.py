from .serializers import *
from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth.models import User
from server.authenticate import Authenticate
from .models import  Posts, Comments, PostLikes
from rest_framework.views import APIView, Response, status

class Authe(APIView):
  def post(self, req):
    username = req.data['phone']
    del req.data['phone']
    try:
      user = User.objects.create_user(username=username, **req.data)
      user = UserSerializer(user).data

      return Response({'status':status.HTTP_201_CREATED, 'data': user})
    except IntegrityError:
      return Response({"status": status.HTTP_409_CONFLICT, "error":"phone already exists"})
    except Exception as err:
      print('error:', err)
      return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': str(err)})


class Post(APIView):
  # permission_classes = (Authenticate,)
  def get(self, req):
    posts = Posts.objects.filter(author_id=1)
    posts = PostSerializer(posts, many=True).data

    return Response({'status': status.HTTP_200_OK, 'posts': posts})

  def post(self, req):
    print('user: ', req)
    post = Posts.objects.create(author_id=1 , **req.data)
    post = PostSerializer(post).data

    return Response({'status': status.HTTP_201_CREATED, 'posts': post})


  def put(self, req, post_id=None):
    if post_id is not None:
      try:
        Posts.objects.filter(id=post_id).update(**req.data)

        post = Posts.objects.get(id=post_id)
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
    comment = Comments.objects.create(user_id= 1, post_id=post_id , **req.data)
    comment = CommentSerializer(comment).data

    return Response({'status': status.HTTP_201_CREATED, 'comment': comment})
  
  def put(self, req, comment_id=None):
    if comment_id is not None:
      try:
        Comments.objects.filter(id=comment_id).update(**req.data)

        comment = Comments.objects.get(id=comment_id)
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
    if len(post_like) == 0:
      PostLikes.objects.create(post_id=post_id, user_id=1)
      return Response(status=status.HTTP_200_OK)
    else:
      PostLikes.objects.get(post_id=post_id, user_id=1).delete()
      return Response(status=status.HTTP_200_OK)