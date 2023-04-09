from django.urls import path
from store.views import *

urlpatterns=[
    path("category/",CategoryList.as_view(),name="list"),
    path("product/",ProductList.as_view(),name="list"),
    path("product/<int:id>/",ProductDetail.as_view(),name="detail"),
]