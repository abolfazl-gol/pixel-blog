from django.urls import path
from store.views import *

urlpatterns=[
    path("store/category/",CategoryList.as_view(),name="list"),
    path("store/product/",ProductList.as_view(),name="list"),
    path("store/product/<int:id>/",ProductDetail.as_view(),name="detail"),
    path("checkout/cart/", CartListCreate.as_view(),name="list"),
    path("checkout/cart<int:id>/", CartDetail.as_view(), name="detail"),
    path("payment/", OrderListCreate.as_view(), name="list"),
    path("payment/verify/", PaymentVerifyCreate.as_view(), name="list"),
    path("order/<int:id>/", OrderDetail.as_view(), name="detail")
]