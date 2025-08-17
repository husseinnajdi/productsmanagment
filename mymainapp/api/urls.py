from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('products', views.ProductsView, basename='products')
router.register('orders',views.OrderView,basename='orders')
router.register('orderitem',views.OrderItemView,basename='orderitem')

urlpatterns=[
    path('',include(router.urls))
]