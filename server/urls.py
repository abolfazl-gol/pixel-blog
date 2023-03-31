from django.contrib import admin
from django.urls import path
from blog import views as blog_view
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', blog_view.Authe.as_view()),
    path('posts/',  blog_view.Post.as_view()),
    path('posts/<int:post_id>/',  blog_view.Post.as_view()),
    path('posts/<int:post_id>/like/',  blog_view.PostLike.as_view()),
    path('posts/<int:post_id>/comment/',  blog_view.Comment.as_view()),
    path('posts/<int:post_id>/comment/<int:comment_id>/',  blog_view.Comment.as_view()),
]
