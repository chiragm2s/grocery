from rest_framework import views
from .views import RegisterAPI,LoginAPI,ProductView,DemoView,OrderView,DeliveryView
from django.urls import path
from django.conf.urls import url
from knox import views as knox_views
from django.urls import path
from groceryapp import views

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('products' , ProductView.as_view() ),
    path('demo' , DemoView.as_view()),
    path('orders' , OrderView.as_view()),
    path('delivery' , DeliveryView.as_view()),
    url('productstest' , views.productsyerapi ),
    url('ordertest' , views.orderapi ),
    url('carttest' , views.cartapi ),
    url('deliverytest' , views.deliveryapi ),
    url('deliveryAssignedtest' , views.deliverAssignedyapi ),
    url('login' , views.LoginAPI ),
    url('login' , views.RegisterAPI ),


]
