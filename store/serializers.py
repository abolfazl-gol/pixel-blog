from store.models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        

class ProductSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        if validated_data['price'] >= 1000:
            product = Product.objects.create(**validated_data)
            print('product: ', product)
            return product
        else:
            raise serializers.ValidationError("price kamtar az 1000 toman ast")

    class Meta:
        model = Product
        fields = "__all__"



