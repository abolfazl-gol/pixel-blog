from django.shortcuts import render
from store.models import *
from store.serializers import *
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class CategoryList(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductList(ListCreateAPIView):
    # model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_paginated_response(self, data):
        print('dtat: ', data)
        if self.request.accepted_renderer.format == 'html':
            return 3
        return 5

        return super().get_paginated_response(data)
class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"
