from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('products', views.ProductsView, basename='products')
router.register('orders',views.OrderView,basename='orders')

urlpatterns=[
    path('',include(router.urls))
]