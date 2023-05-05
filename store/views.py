import random
from store.models import *
from store.serializers import *
from store.pagination import *
from rest_framework.views import Response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404


class CategoryList(ListCreateAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination

    def filter_queryset(self, queryset):
        paginator = self.parser_classes()
        result_page = paginator.paginate_queryset(queryset, self.request)
        serializer = CategorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        paginator = CategoryPagination
        pq = paginator.paginate_queryset(self, queryset, request)
        serializer = CategorySerializer(pq, many=True)
        return paginator.get_paginated_response(serializer.data)
    

class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"


class CartListCreate(ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    # permission_classes = (IsAuthenticated,)
     
    def filter_queryset(self, queryset):
        queryset = queryset.filter(user_id=1)
        return super().filter_queryset(queryset)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cart_id = response.data.get('id')
        cart_item = request.data['item']
        try:
            product = Product.objects.get(id=cart_item['product_id'])
            # add itme to CartProduct table
            CartProduct.objects.create(cart_id=cart_id,product_id=product.id, price=product.price, quantity=cart_item['quantity'])
        except Product.DoesNotExist:
            return Response({'error': 'product not found'}, status=status.HTTP_404_NOT_FOUND)

        return response

class CartDetail(RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        cart = super().patch(request, *args, **kwargs)
        if cart.data.get('checkout'):
            return Response({'error':'this shopping cart has been paid'}, status=status.HTTP_400_BAD_REQUEST)

        cart_product = get_object_or_404(CartProduct, id=request.data['itme_id'],cart_id=kwargs['id'])
        if 'increment' in request.data:
            cart_product.quantity += 1
            cart_product.save()
        elif 'decrement' in request.data:
            cart_product.quantity -= 1
            cart_product.save()
        return cart

    def delete(self, request, *args, **kwargs):
        cart_product = get_object_or_404(CartProduct, id=request.data['itme_id'],cart_id=kwargs['id'])
        print('cart_product: ', cart_product)
        cart_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderListCreate(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def filter_queryset(self, queryset):
        queryset = queryset.filter(user_id=1)
        return super().filter_queryset(queryset)

    def create(self, request, *args, **kwargs):
        user_id=self.request.user.id
        cart_id = request.data['cart_id']

        cart = get_object_or_404(Cart, id=cart_id, user_id=1, checkout=False)
        address = get_object_or_404(Address, id=request.data['address_id'], user_id=1)
        raw_query = CartProduct.objects.raw('SELECT id, SUM(price * quantity) total FROM cart_products WHERE cart_id= %s',[cart_id])[0]

        request.data['total'] = raw_query.total
        request.data['address'] = address.id
        request.data['cart'] = cart.id
        order_resp = super().create(request, *args, **kwargs)

        result = create_payment(raw_query.total, order_resp.data.get('id'))

        Order.objects.filter(id=order_resp.data.get('id'),cart_id=cart_id,).update(payment_id=result['id'])
        
        return Response({'link': result['link']}, status=status.HTTP_200_OK)

class OrderDetail(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        user_id = self.request.user.id
        order = Order.objects.filter(id=kwargs['id'], user_id=1).update(status=request.data['status'])

        return Response(order, status=status.HTTP_200_OK)
    

class PaymentVerifyCreate(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        user_id = self.request.user.id
        order_id = request.data['id']
        payment_id = request.data['payment_id']
        order = get_object_or_404(Order, id=order_id, payment_id=payment_id)

        result = verify_payment(order_id, payment_id)
        print('result:', result)
        if result['status'] == 100:
            Order.objects.filter(id=order_id,user_id=1).update(payment_status="success")
            Cart.objects.filter(id=order.cart_id).update(checkout=True)

            return Response({'message': result['message']}, status=status.HTTP_200_OK)

        else:
            Order.objects.filter(id=order_id,user_id=1).update(payment_status="fail")
            return Response({'message': result['message']}, status=status.HTTP_417_EXPECTATION_FAILED)





def create_payment(amount, order_id):
    result = {'order_id': order_id,'amount': amount,'callback': 'http://localhost:8000/payment/verify'}

    return {'id': '198737313', 'link': 'http://localhost:8000/payment/verify'}

def verify_payment(payment_id, order_id):
    result = '/payment/verify', { id: payment_id, order_id:order_id }
    
    random_status = [{'status': 100, 'message':'پرداخت تایید شده است'}, {'status': 1, 'message':'پرداخت انجام نشده است'}]
    return random.choice(random_status)
