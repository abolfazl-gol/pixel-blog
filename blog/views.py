from .models import *
from .serializers import *
from django.db import transaction
from django.shortcuts import render
from app.authenticate import Authenticate
from rest_framework.views import APIView, Response, status
from rest_framework.parsers import MultiPartParser, FormParser


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
      post['comments'] = {'total_records': total_records,'pages': pages,'data': CommentSerializer(comments, many=True).data}

      posts.append(post)

    return Response(posts, status=status.HTTP_200_OK)


  def post(self, req):
    if 'image' in req.data:
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
            return Response({'error':image_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

          return Response({**post, 'image': image_serializer.data['image']}, status=status.HTTP_201_CREATED)
      except Exception as err:
        return Response({'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)
    else:
      post = Post.objects.create(author_id=req.user.id , **data)
      post = PostSerializer(post).data
      return Response(post, status=status.HTTP_201_CREATED)
    

  def put(self, req, post_id=None):
    if post_id is not None:
      try:
        Post.objects.filter(id=post_id).update(**req.data)

        post = Post.objects.get(id=post_id)
        post = PostSerializer(post).data

        return Response(post, status=status.HTTP_200_OK)
      except Post.DoesNotExist:
        return Response({'error': 'post not found'}, status=status.HTTP_404_NOT_FOUND)
      except Exception as err:
        return Response({'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)
    else:
      return Response(status=status.HTTP_400_BAD_REQUEST)
    
  
  def delete(self, req, post_id):
    if post_id is not None:
      try:
        Post.objects.get(id=post_id).delete()
        return Response(status=status.HTTP_200_OK)
      except Post.DoesNotExist:
        return Response({'error': 'post not found'}, status=status.HTTP_404_NOT_FOUND)
      except Exception as err:
        return Response({'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)
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

      return Response({'total_records': total_records,'pages': pages,'data':comments}, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
      return Response({'error': 'post id not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as err:
      return Response({'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)
  
  def post(self, req, post_id=None):
    comment = Comment.objects.create(user_id= req.user.id, post_id=post_id , **req.data)
    comment = CommentSerializer(comment).data

    return Response(comment, status=status.HTTP_201_CREATED)
  
  def put(self, req, comment_id=None):
    if comment_id is not None:
      try:
        Comment.objects.filter(id=comment_id).update(**req.data)

        comment = Comment.objects.get(id=comment_id)
        comment = CommentSerializer(comment).data

        return Response(comment, status=status.HTTP_200_OK)
      except Comment.DoesNotExist:
        return Response({'error': 'comment not found'}, status=status.HTTP_404_NOT_FOUND)
      except Exception as err:
        return Response({'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)
    else:
      return Response(status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self, req, comment_id):
    if comment_id is not None:
      try:
        Comment.objects.get(id=comment_id, user_id=req.user.id).delete()
        return Response(status=status.HTTP_200_OK)
      except Comment.DoesNotExist:
        return Response({'error': 'comment not found'}, status=status.HTTP_404_NOT_FOUND)
      except Exception as err:
        return Response({'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)
    else:
      return Response(status=status.HTTP_400_BAD_REQUEST)
    

class PostLikeView(APIView):
  def post(self, req, post_id):
    user_id = req.user.id
    post_like = PostLike.objects.filter(post_id=post_id, user_id=user_id).exists()
    if post_like:
      PostLike.objects.get(post_id=post_id, user_id=user_id).delete()
      return Response(status=status.HTTP_200_OK)
    else:
      PostLike.objects.create(post_id=post_id, user_id=user_id)
      return Response(status=status.HTTP_200_OK)