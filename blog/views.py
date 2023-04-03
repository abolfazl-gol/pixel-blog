from .models import *
from .serializers import *
from django.shortcuts import render
from django.contrib.auth.models import User
from server.authenticate import Authenticate
from django.db import IntegrityError, transaction
from rest_framework.views import APIView, Response, status
from rest_framework.parsers import MultiPartParser, FormParser

class AutheView(APIView):
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
      return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': str(err)})

  def put(self, req):
    User.objects.filter(id=req.user.id).update(**req.data)
    user = User.objects.get(id=req.user.id)
    user = UserSerializer(user).data
      
    return Response({'status':status.HTTP_200_OK, 'data': user})

class PostView(APIView):
  permission_classes = (Authenticate,)
  parser_classes = (MultiPartParser, FormParser)


  def get(self, req):
    page = 1 if 'page' not in req.GET else int(req.GET['page'])
    size = 20 if 'size' not in req.GET else int(req.GET['size'])
    if size > 50: size = 50

    posts = Post.objects.filter(author_id=req.user.id)
    serialized_posts = PostSerializer(posts, many=True).data
    
    posts = []
    for post in serialized_posts:
      post = dict(post)
      likes_count = PostLike.objects.filter(post_id=post['id']).count()
      post['likes_count'] = likes_count

      comments = Comment.objects.filter(post_id=post['id']).order_by('id')[page:size]
      total_records = Comment.objects.filter(post_id=post['id']).count()
      pages = total_records // size
      if total_records % size > 0: pages +=1
      post['comments'] = {'total_records': total_records,'pages': pages,'itmes':CommentSerializer(comments, many=True).data}

      posts.append(post)

    return Response({'status': status.HTTP_200_OK, 'posts': posts})


  def post(self, req):
    image = req.data['image']
    del req.data['image']
   
    data = { key: req.data[key] for key in req.data }

    try:
      with transaction.atomic():
        post = Post.objects.create(author_id=req.user.id , **data)
        post = PostSerializer(post).data
        image_serializer = ImageSerializer(data={"image": image, "post": post['id']})
        if image_serializer.is_valid():
          image_serializer.save()
        else:
          transaction.set_rollback(True)
          return Response({'status':status.HTTP_400_BAD_REQUEST, 'error':image_serializer.errors})

        return Response({'status': status.HTTP_201_CREATED, 'post': {**post, 'image': image_serializer.data['image']}})
    except Exception as err:
      return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': str(err)})

  def put(self, req, post_id=None):
    if post_id is not None:
      try:
        Post.objects.filter(id=post_id).update(**req.data)

        post = Post.objects.get(id=post_id)
        post = PostSerializer(post).data

        return Response({'status':status.HTTP_200_OK, 'post':post})
      except Post.DoesNotExist:
        return Response({'status': status.HTTP_404_NOT_FOUND, 'error': 'post not found'})
      except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': str(err)})
    else:
      return Response(status=status.HTTP_400_BAD_REQUEST)
    
  
  def delete(self, req, post_id):
    if post_id is not None:
      try:
        Post.objects.get(id=post_id).delete()
        return Response(status=status.HTTP_200_OK)
      except Post.DoesNotExist:
        return Response({'status': status.HTTP_404_NOT_FOUND, 'error': 'post not found'})
      except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': str(err)})
    else:
      return Response(status=status.HTTP_400_BAD_REQUEST)
    
class CommentView(APIView):
  permission_classes = (Authenticate,)

  def get(self, req, post_id=None):
    page = 1 if 'page' not in req.GET else int(req.GET['page'])
    size = 20 if 'size' not in req.GET else int(req.GET['size'])
    if size > 50: size = 50

    try:
      comments = Comment.objects.filter(post_id=post_id).order_by('id')[page:size]
      comments = CommentSerializer(comments, many=True).data
      
      total_records = Comment.objects.filter(post_id=post_id).count()
      pages = total_records // size
      if total_records % size > 0: pages +=1

      return Response({'status': status.HTTP_200_OK, 'total_records': total_records,'pages': pages,'itmes':comments})
    except Comment.DoesNotExist:
      return Response({'status': status.HTTP_404_NOT_FOUND, 'error': 'post id not found'})
    except Exception as err:
      return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': str(err)})
  
  def post(self, req, post_id=None):
    comment = Comment.objects.create(user_id= req.user.id, post_id=post_id , **req.data)
    comment = CommentSerializer(comment).data
    print('post:', comment['post'])
    return Response({'status': status.HTTP_201_CREATED, 'comment': comment})
  
  def put(self, req, comment_id=None):
    if comment_id is not None:
      try:
        Comment.objects.filter(id=comment_id).update(**req.data)

        comment = Comment.objects.get(id=comment_id)
        comment = CommentSerializer(comment).data

        return Response({'status':status.HTTP_200_OK, 'comment':comment})
      except Comment.DoesNotExist:
        return Response({'status': status.HTTP_404_NOT_FOUND, 'error': 'comment not found'})
      except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': str(err)})
    else:
      return Response(status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self, req, comment_id):
    if comment_id is not None:
      try:
        Comment.objects.get(id=comment_id, user_id=req.user.id).delete()
        return Response(status=status.HTTP_200_OK)
      except Comment.DoesNotExist:
        return Response({'status': status.HTTP_404_NOT_FOUND, 'error': 'comment not found'})
      except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': str(err)})
    else:
      return Response(status=status.HTTP_400_BAD_REQUEST)
    

class PostLikeView(APIView):
  def post(self, req, post_id):
    user_id = req.user.id
    post_like = PostLike.objects.filter(post_id=post_id, user_id=user_id)
    if len(post_like) == 0:
      PostLike.objects.create(post_id=post_id, user_id=user_id)
      return Response(status=status.HTTP_200_OK)
    else:
      PostLike.objects.get(post_id=post_id, user_id=user_id).delete()
      return Response(status=status.HTTP_200_OK)