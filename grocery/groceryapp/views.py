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
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework import status


# Register API
# class RegisterAPI(generics.GenericAPIView):
#     serializer_class = RegisterSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response({
#         "user": UserSerializer(user, context=self.get_serializer_context()).data,
#         "token": AuthToken.objects.create(user)[1]
#         })


class RegisterAPI(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        # law_data = JSONParser().parse(request)
        # serializer=UserRegisterSerializer(data=law_data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "data": serializer.data,
                "message": "User Created Successfully.",
                "status":status.HTTP_201_CREATED,
                "token": AuthToken.objects.create(user)[1]
            })
        return Response({
                "error": serializer.errors,
                "message": "Some thing Went Wrong",
                "status":status.HTTP_400_BAD_REQUEST
            })

#for login api
# class LoginAPI(KnoxLoginView):
#     permission_classes = (permissions.AllowAny)

#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
        
#         #qs = User.objects.values_list('is_admin', 'email')
#         login(request, user)
#         return super(LoginAPI, self).post(request, format=None)


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            alldetails=User.objects.all().filter(username=request.data["username"]).values('is_admin')
            # print(type(alldetails))    
            login(request, user)
            # return super(LoginAPI, self).post(request, format=None)
            return Response({
                "status":status.HTTP_202_ACCEPTED,
                "data": alldetails,
                "message": "Login Successfully.",
                "token": AuthToken.objects.create(user)[1],
            })
        return Response({
                "status":status.HTTP_400_BAD_REQUEST,
                "error": serializer.errors,
                "message": "Some thing Went Wrong",                
            })


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
        cart_serializer=CartSerializer(cartvariable,many=True)
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
@csrf_exempt
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
        deliverysapi=DeliverySerializer(data=delivery_data)
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
        deliveryAssignedvariable = delivery_assigned.objects.all()
        delivryAssigned_serializer=DeliveryAssignedSerializer(deliveryAssignedvariable,many=True)
        #orderapi_data=JSONParser().parse(request)
        # ordersapi=products.objects.get(id=orderapi_data['id'])
        # ordersapiserializers=OrderSerializer(ordersapi)
        # # result=type(data)
        # # print(result)
        return JsonResponse(delivryAssigned_serializer.data,safe=False)

    elif request.method=='POST':
        deliveryAssigned_data=JSONParser().parse(request)
        deliverysapi=DeliveryAssignedSerializer(data=deliveryAssigned_data)
        #print(productsapiserializers)
        if deliverysapi.is_valid(raise_exception=False):
            deliverysapi.save()
            return JsonResponse("data added succesfully",safe=False)
        errors = {
            "message":deliverysapi.errors,"status":401
        }
        return JsonResponse(errors,safe=False)

#for products swagger

class productsgeneric(generics.GenericAPIView):
    serializer_class = ProductSerializer
    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        # law_data = JSONParser().parse(request)
        # serializer=UserRegisterSerializer(data=law_data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "data": serializer.data,
                "message": "products added Successfully.",
                "status":status.HTTP_201_CREATED,
                "token": AuthToken.objects.create(user)[1]
            })
        return Response({
                "error": serializer.errors,
                "message": "Some thing Went Wrong",
                "status":status.HTTP_400_BAD_REQUEST
            })
#for prduct post image
class productpost(APIView):
    permissions_classes=[permissions.IsAuthenticated]
    parsers_classes=[MultiPartParser,FormParser]
    def post(self,request,format=None): 
        print(request.data)
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            result = {
                "status": status.HTTP_202_ACCEPTED,
                "data": serializer.data,
                "message": " Detials updated Successfully",
                
                }
            return Response(result)
        else:
            error={
                "message":"something went wrong",
                "data": serializer.errors,
                "status":status.HTTP_400_BAD_REQUEST,
            }
            return Response(error)


#for products get image
class productget(APIView):
    def get(self,request,pk,*args, **kwargs):
        try: 
            prod = products.objects.get(pk=pk) 
        except products.DoesNotExist: 
            return JsonResponse({'message': 'Detials does not exist',"status": 404}, status=status.HTTP_404_NOT_FOUND) 

        if request.method == 'GET':
            prodSerializer = ProductSerializer(prod) 
            # return JsonResponse(tutorial_serializer.data) 

            result = {
                "status": 201,
                "data": prodSerializer.data,
                "message": " Detials Fetched Successfully",
                
                }
            return JsonResponse(result,safe=False)
        # return JsonResponse("result",safe=False)

#for orders swagger
class ordersgeneric(generics.GenericAPIView):
    serializer_class = OrderSerializer
    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        # law_data = JSONParser().parse(request)
        # serializer=UserRegisterSerializer(data=law_data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "data": serializer.data,
                "message": "orders saved Successfully.",
                "status":status.HTTP_201_CREATED,
                "token": AuthToken.objects.create(user)[1]
            })
        return Response({
                "error": serializer.errors,
                "message": "Some thing Went Wrong",
                "status":status.HTTP_400_BAD_REQUEST
            })

class orderupdate(APIView):
    parsers_classes=[MultiPartParser,FormParser]
    def put(self,request,pk,format=None):
        if request.method=='PUT':
            print(request.data)
            #weightable_data = JSONParser().parse(request)
            orderdata = orders.objects.get(pk=pk)
            ordertable_serializer = OrderSerializer(orderdata,data=request.data,partial=True)
            if ordertable_serializer.is_valid():
                ordertable_serializer.save()
                success={
                    "message" :" Detials Updated Successfully",
                    "status" : status.HTTP_200_OK,
                    "data" : ordertable_serializer.errors,
                }
                return Response(success)
            error={
                "message":ordertable_serializer.errors,
                "status":status.HTTP_400_BAD_REQUEST,
            }
            return Response(error)

#for delivery swagger
class deliverygeneric(generics.GenericAPIView):
    serializer_class = DeliverySerializer
    def post(self, request, *args, **kwargs):
        serializer = DeliverySerializer(data=request.data)
        # law_data = JSONParser().parse(request)
        # serializer=UserRegisterSerializer(data=law_data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "data": serializer.data,
                "message": "orders saved Successfully.",
                "status":status.HTTP_201_CREATED,
                "token": AuthToken.objects.create(user)[1]
            })
        return Response({
                "error": serializer.errors,
                "message": "Some thing Went Wrong",
                "status":status.HTTP_400_BAD_REQUEST
            })
#api for delivery update
class deliveryupdate(APIView):
    parsers_classes=[MultiPartParser,FormParser]
    def put(self,request,pk,format=None):
        if request.method=='PUT':
            print(request.data)
            #weightable_data = JSONParser().parse(request)
            deliverydata = delivery.objects.get(pk=pk)
            deliverytable_serialzer = DeliverySerializer(deliverydata,data=request.data,partial=True)
            if deliverytable_serialzer.is_valid():
                deliverytable_serialzer.save()
                success={
                    "message" :" Detials Updated Successfully",
                    "status" : status.HTTP_200_OK,
                    "data" : deliverytable_serialzer.errors,
                }
                return Response(success)
            error={
                "message":deliverytable_serialzer.errors,
                "status":status.HTTP_400_BAD_REQUEST,
            }
            return Response(error)

#for deliveryAssigned swagger
class deliveryAssignedgeneric(generics.GenericAPIView):
    serializer_class = DeliveryAssignedSerializer
    def post(self, request, *args, **kwargs):
        serializer = DeliveryAssignedSerializer(data=request.data)
        # law_data = JSONParser().parse(request)
        # serializer=UserRegisterSerializer(data=law_data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "data": serializer.data,
                "message": "orders saved Successfully.",
                "status":status.HTTP_201_CREATED,
                "token": AuthToken.objects.create(user)[1]
            })
        return Response({
                "error": serializer.errors,
                "message": "Some thing Went Wrong",
                "status":status.HTTP_400_BAD_REQUEST
            })

#api for delivery Assigned update
class deliveryassignedupdate(APIView):
    parsers_classes=[MultiPartParser,FormParser]
    def put(self,request,pk,format=None):
        if request.method=='PUT':
            print(request.data)
            #weightable_data = JSONParser().parse(request)
            deliverassignedydata = delivery_assigned.objects.get(pk=pk)
            deliverytableassigned_serialzer = DeliveryAssignedSerializer(deliverassignedydata,data=request.data,partial=True)
            if deliverytableassigned_serialzer.is_valid():
                deliverytableassigned_serialzer.save()
                success={
                    "message" :" Detials Updated Successfully",
                    "status" : status.HTTP_200_OK,
                    "data" : deliverytableassigned_serialzer.errors,
                }
                return Response(success)
            error={
                "message":deliverytableassigned_serialzer.errors,
                "status":status.HTTP_400_BAD_REQUEST,
            }
            return Response(error)

#for authentication
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import login
from knox.auth import TokenAuthentication
# from knox.views import LoginView as KnoxLoginView
from .utils import phone_validator, password_generator, otp_generator
from .serializers import (CreateUserSerializer, ChangePasswordSerializer,
                          UserSerializer, LoginUserSerializer, ForgetPasswordSerializer)
from groceryapp.models import User, PhoneOTP
from django.shortcuts import get_object_or_404
from django.db.models import Q
import requests