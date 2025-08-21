from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import ProductSerializer,OrderSeriaizer,OrderItemSerializer
from products.models import Product
from orders.models import Order,OrderItem
from decouple import config
from groq import Groq
from rest_framework.decorators import action

client = Groq(api_key=config("GroqAI_API_Key"))
class ProductsView(viewsets.ViewSet):
    @action(detail=True, methods=["get"])
    def ai_summary(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        prompt = f"Give me a short marketing description for: {product.product_name} that is description is {product.product_description}."

        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",   
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100
            )
            return Response({
                "product_id": product.id,
                "ai_summary": response.choices[0].message.content.strip()
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)

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
    @action(detail=True,methods=["get"])
    def ai_summery(self,request,pk=None):
        order=get_object_or_404(Order,pk=pk)
        items = order.items.all()

    # Build a clear list of items for the AI
        items_text = "\n".join([
            f"- Product {item.product_id}, Quantity: {item.quantity}, Price: {item.price}"
            for item in items
        ])

        prompt = f"""
        A customer placed an order with ID {order.id}.
        The items are:
        {items_text}

    Please calculate the total price and summarize this order in one short sentence.
    """
        try:
            response=client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role":"system","content":"You are a helpful assistant."},
                    {"role":"user","content":prompt}
                ],
                max_tokens=100
            )
            return Response({
                "product_id": order.id,
                "ai_summary": response.choices[0].message.content.strip()
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)
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