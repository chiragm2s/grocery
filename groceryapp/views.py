from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

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
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
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
#for products.api.
@csrf_exempt
def productsyerapi(request,id=0):
    if request.method=='GET':
        # students = products.objects.all()
        # students_serializer=ProductSerializer(students,many=True)
        productsapi_data=JSONParser().parse(request)
        productsapi=products.objects.get(id=productsapi_data['id'])
        productsapiserializers=ProductSerializer(productsapi)
        # # result=type(data)
        # # print(result)
        return JsonResponse(productsapiserializers.data,safe=False)

    elif request.method=='POST':
        productsapi_data=JSONParser().parse(request)
        productsapiserializers=ProductSerializer(data=productsapi_data)
        #print(productsapiserializers)
        if productsapiserializers.is_valid(raise_exception=False):
            productsapiserializers.save()
            return JsonResponse("data added succesfully",safe=False)
        errors = {
            "message":productsapiserializers.errors,"status":401
        }
        return JsonResponse(errors,safe=False)

#for orders.api.
@csrf_exempt
def orderapi(request,id=0):
    if request.method=='GET':
        ordervariable = orders.objects.all()
        order_serializer=OrderSerializer(ordervariable,many=True)
        #orderapi_data=JSONParser().parse(request)
        # ordersapi=products.objects.get(id=orderapi_data['id'])
        # ordersapiserializers=OrderSerializer(ordersapi)
        # # result=type(data)
        # # print(result)
        return JsonResponse(order_serializer.data,safe=False)

    elif request.method=='POST':
        orderapi_data=JSONParser().parse(request)
        ordersapi=OrderSerializer(data=orderapi_data)
        #print(productsapiserializers)
        if ordersapi.is_valid(raise_exception=False):
            ordersapi.save()
            return JsonResponse("data added succesfully",safe=False)
        errors = {
            "message":ordersapi.errors,"status":401
        }
        return JsonResponse(errors,safe=False)
#for cart.api
@csrf_exempt
def cartapi(request,id=0):
    if request.method=='GET':
        cartvariable = Cart.objects.all()
        cart_serializer=OrderSerializer(cartvariable,many=True)
        #orderapi_data=JSONParser().parse(request)
        # ordersapi=products.objects.get(id=orderapi_data['id'])
        # ordersapiserializers=OrderSerializer(ordersapi)
        # # result=type(data)
        # # print(result)
        return JsonResponse(cart_serializer.data,safe=False)

    elif request.method=='POST':
        cartapi_data=JSONParser().parse(request)
        cartsapi=CartSerializer(data=cartapi_data)
        #print(productsapiserializers)
        if cartsapi.is_valid(raise_exception=False):
            cartsapi.save()
            return JsonResponse("data added succesfully",safe=False)
        errors = {
            "message":cartsapi.errors,"status":401
        }
        return JsonResponse(errors,safe=False)

#for delivery.api
def deliveryapi(request,id=0):
    if request.method=='GET':
        deliveryvariable = delivery.objects.all()
        delivry_serializer=DeliverySerializer(deliveryvariable,many=True)
        #orderapi_data=JSONParser().parse(request)
        # ordersapi=products.objects.get(id=orderapi_data['id'])
        # ordersapiserializers=OrderSerializer(ordersapi)
        # # result=type(data)
        # # print(result)
        return JsonResponse(delivry_serializer.data,safe=False)

    elif request.method=='POST':
        delivery_data=JSONParser().parse(request)
        deliverysapi=CartSerializer(data=delivery_data)
        #print(productsapiserializers)
        if deliverysapi.is_valid(raise_exception=False):
            deliverysapi.save()
            return JsonResponse("data added succesfully",safe=False)
        errors = {
            "message":deliverysapi.errors,"status":401
        }
        return JsonResponse(errors,safe=False)


#for deliveryassigned.api
@csrf_exempt
def deliverAssignedyapi(request,id=0):
    if request.method=='GET':
        deliveryAssignedvariable = delivery.objects.all()
        delivryAssigned_serializer=DeliveryAssignedSerializer(deliveryAssignedvariable,many=True)
        #orderapi_data=JSONParser().parse(request)
        # ordersapi=products.objects.get(id=orderapi_data['id'])
        # ordersapiserializers=OrderSerializer(ordersapi)
        # # result=type(data)
        # # print(result)
        return JsonResponse(delivryAssigned_serializer.data,safe=False)

    elif request.method=='POST':
        deliveryAssigned_data=JSONParser().parse(request)
        deliverysapi=CartSerializer(data=deliveryAssigned_data)
        #print(productsapiserializers)
        if deliverysapi.is_valid(raise_exception=False):
            deliverysapi.save()
            return JsonResponse("data added succesfully",safe=False)
        errors = {
            "message":deliverysapi.errors,"status":401
        }
        return JsonResponse(errors,safe=False)