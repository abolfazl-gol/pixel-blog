from django.db import models
from account.models import Address
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250)
    parent_id = models.IntegerField(default=0)
    class Meta:
        db_table = 'categorys'
    
    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=250)
    images = models.ImageField(upload_to='store/images')
    price = models.IntegerField()
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, db_column='category_id', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
    checkout = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'

    def __str__(self):
        return self.user.username

class Order(models.Model):
    user = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, db_column='cart_id', on_delete=models.CASCADE)
    address = models.ForeignKey(Address, db_column='address_id', on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default='pending')
    total = models.IntegerField()
    payment_id = models.CharField(max_length=255, default='')
    payment_status = models.CharField(max_length=255, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return self.total

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, db_column='cart_id', on_delete=models.CASCADE,related_name='cart_products')
    product = models.ForeignKey(Product, db_column='product_id', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart_products'

    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return self.product.name
    

class Attribute(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'attributes'
    
    def __str__(self):
        return self.name

class Image(models.Model):
  image = models.ImageField(upload_to='blog/images')
  product = models.ForeignKey(Product, db_column='product_id', on_delete=models.CASCADE)

  class Meta:
    db_table = 'product_images'

  def __str__(self):
    return self.image
  

class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, db_column='attribute_id', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, db_column='product_id', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'attribute_values'
    
    def __str__(self):
        return self.value
    
class CartProductValue(models.Model):
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    cart_product = models.ForeignKey(CartProduct, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart_product_values'
    
    def __str__(self):
        return self.value

class Payment(models.Model):
    user = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
    amount = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    authority = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return self.amount