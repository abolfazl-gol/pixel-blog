from django.contrib import admin
from django.urls import path
from blog import views as blog_view
from django.conf.urls.static import static
from .settings import DEBUG, MEDIA_ROOT, MEDIA_URL
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', blog_view.AutheView.as_view()),
    path('posts/',  blog_view.PostView.as_view()),
    path('posts/<int:post_id>/',  blog_view.PostView.as_view()),
    path('posts/<int:post_id>/like/',  blog_view.PostLikeView.as_view()),
    path('posts/<int:post_id>/comment/',  blog_view.CommentView.as_view()),
    path('posts/<int:post_id>/comment/<int:comment_id>/',  blog_view.CommentView.as_view()),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)