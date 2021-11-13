from django.shortcuts import render

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
#from .serializers import UserSerializer, RegisterSerializer
#below for login
from django.contrib.auth import login
import pickle
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

from . models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView

from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

#for login api
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        #qs = User.objects.values_list('is_admin', 'email')
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

    #products

class DemoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self ,request):
         print(request.user)
         return Response({'sucess' : "Hurray you are authenticated"})

class ProductView(APIView):
    
    def get(self,request):
        category = self.request.query_params.get('category')
        if category:
            queryset = products.objects.filter(category__category_name =  category)
        else:
            queryset = products.objects.all()
        serializer = ProductSerializer(queryset , many = True)
        return Response({'count' : len(serializer.data) ,'data' :serializer.data})


class OrderView(APIView):
    
    def get(self,request):
        username = self.request.query_params.get('username')
        if username:
            queryset = orders.objects.filter(User__user_name =  username)
        else:
            queryset = orders.objects.all()
        serializer = OrderSerializer(queryset , many = True)
        return Response({'count' : len(serializer.data) ,'data' :serializer.data})


class DeliveryView(APIView):
    
    def get(self,request):
        username = self.request.query_params.get('username')
        if username:
            queryset = delivery.objects.filter(User__user_name =  username)
        else:
            queryset = delivery.objects.all()
        serializer = DeliverySerializer(queryset , many = True)
        return Response({'count' : len(serializer.data) ,'data' :serializer.data})

