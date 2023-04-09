from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import base.views
from account.models import *
from account.serializers import *
from django.db import IntegrityError
from app.authenticate import Authenticate



class AutheView(APIView):
    # permission_classes = (Authenticate,)
    def get(self, request, user_id=None):
        if request.user.is_staff:
            if user_id is None:
                return Response({"message": "User with this profile was not found!"},
                                status=status.HTTP_400_BAD_REQUEST)

            user = Profile.objects.get(user_id=user_id)
            user_serializer = UserSerializer(user).data

            return Response(user_serializer, status=status.HTTP_302_FOUND)
        else:
            # user = Profile.objects.get(id=request.user.id)           # error: permission

            return Response({"message": "access denied"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            user = User.objects.create_user(username=request.data["username"], password=request.data["password"])
            profile = Profile.objects.create(user_id=user.id)
            user = UserSerializer(user).data

            return Response(user, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "username already exists"}, status=status.HTTP_409_CONFLICT)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, req):

        if req.user and req.user.is_authenticated:
            user = User.objects.filter(id=req.user.id).update(**req.data)
            user = User.objects.get(id=req.user.id)
            user = UserSerializer(user).data

            return Response(user, status=status.HTTP_200_OK)
        else:
            return Response({"message": "access denied"}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        if request.user.is_staff:
            try:
                user = User.objects.get(id=request.data["id"])
                # user.delete()
                return Response({"message": "user {} deleted successfully".format(request.data["id"])},
                                status=status.HTTP_200_OK)
            except:
                return Response({"message": "user {} not exist".format(request.data["id"])},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "access denied"}, status=status.HTTP_400_BAD_REQUEST)