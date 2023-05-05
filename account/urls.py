from django.urls import path
from account.views import *
from django.conf import settings
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', AutheView.as_view()),
    path('account/', AutheView.as_view()),

]
