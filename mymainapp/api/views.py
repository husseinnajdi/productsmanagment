from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import ProductSerializer,OrderSeriaizer,OrderItemSerializer
from products.models import Product
from orders.models import Order,OrderItem

class ProductsView(viewsets.ViewSet):
    def list(self,request):
        queryset=Product.objects.all()
        serializer=ProductSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def create(self,request):
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self,request,pk=None):
        product=get_object_or_404(Product,pk=pk)
        serializer=ProductSerializer(product)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def update(self,request,pk=None):
        product=get_object_or_404(Product,pk=pk)
        serializer=ProductSerializer(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk=None):
        product=get_object_or_404(Product,pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class OrderView(viewsets.ViewSet):
    def list(self,request):
        queryset=Order.objects.all()
        serializer=OrderSeriaizer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def create(self,request):
        serializer=OrderSeriaizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self,request,pk=None):
        order=get_object_or_404(Order,pk=pk)
        serializer=OrderSeriaizer(order)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def update(self,request,pk=None):
        order=get_object_or_404(Order,pk=pk)
        serializer=OrderSeriaizer(order,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk=None):
        order=get_object_or_404(Order,pk=pk)
        order.delete()
        return Response(status=status.HTTP_200_OK)

class OrderItemView(viewsets.ViewSet):
    def list(self,request):
        queryset=OrderItem.objects.all()
        serializer=OrderItemSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def create(self,request):
        serializer=OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self,request,pk=None):
        orderitem=get_object_or_404(OrderItem,pk=pk)
        serializer=OrderItemSerializer(orderitem)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def update(self,request,pk=None):
        order=get_object_or_404(OrderItem,pk=pk)
        serializer=OrderItemSerializer(order,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk=None):
        order=get_object_or_404(OrderItem,pk=pk)
        order.delete()
        return Response(status=status.HTTP_200_OK)