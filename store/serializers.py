from store.models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
  def create(self, validated_data):
    if 'parent_id' in validated_data and not Category.objects.filter(id=validated_data['parent_id']).exists():
        raise serializers.ValidationError('parnet_id not found')

    return super().create(validated_data)
  class Meta:
    model = Category
    fields = '__all__'


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
    fields = '__all__'


class CartProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = CartProduct
    fields = ['id', 'price', 'quantity', 'created_at', 'updated_at']


class CartSerializer(serializers.ModelSerializer):

  def create(self, validated_data):
    cart = Cart.objects.filter(user_id=validated_data['user']).last()
    if not cart or cart.checkout:
      cart = Cart.objects.create(**validated_data)

    return {'id':cart.pk, 'user':cart.user, 'checkout': cart.checkout}
  
  class Meta:
    model = Cart
    fields = ['id', 'user', 'checkout']


class OrderSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Order
    fields = '__all__'