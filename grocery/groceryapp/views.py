from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404,render
from rest_framework import generics, permissions
from rest_framework import response
from rest_framework.response import Response
from knox.models import AuthToken
#from .serializers import UserSerializer, RegisterSerializer
#below for login
from django.contrib.auth import login
import pickle
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, UpdateView, DetailView, DeleteView, CreateView )
from . models import *
from rest_framework.decorators import api_view, permission_classes
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.views.generic import TemplateView, ListView
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser,FileUploadParser
#for authentication
from rest_framework import permissions, generics, status,views
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from django.contrib.auth import login
# from knox.auth import TokenAuthentication
# from knox.views import LoginView as KnoxLoginView
# from .utils import phone_validator, password_generator, otp_generator
from .serializers import (CreateUserSerializer, ChangePasswordSerializer,
                          UserSerializer, LoginUserSerializer, ForgetPasswordSerializer)
from groceryapp.models import User
from django.views.generic.detail import BaseDetailView
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
from typing import List

#for swagger
# from django.conf import Settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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


#Register View
class RegisterApi(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "status":status.HTTP_201_CREATED,
                "message": "User Created Successfully.",
                "data": serializer.data,
                #"token": AuthToken.objects.create(user)[1]
            })
        return Response({
                "status":status.HTTP_400_BAD_REQUEST,
                "message": "Some thing Went Wrong",                
                "error": serializer.errors,
            })
        
##Login View    
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            alldetails=User.objects.all().filter(email=request.data["email"]).values('id','is_admin','is_customer','is_deliveryboy')
            # print(type(alldetails))    
            login(request, user)
            return Response({
                "status":status.HTTP_202_ACCEPTED,
                "data": alldetails,
                "message": "Login Successfully.",
                #"token": AuthToken.objects.create(user)[1],
            })
        return Response({
                "status":status.HTTP_400_BAD_REQUEST,
                "error": serializer.errors,
                "message": "Some thing Went Wrong",                
            })
        
class logout(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self ,request):
         print(request.user)
         return Response({'sucess' : "Hurray you are authenticated"})

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
    serializer_class = OrderSerializer
    def get(self,request,customerId,productCode):
        try: 
            # lawId = orders.objects.get(customer_id = customerId,product_Code=productCode)
            queryset=orders.objects.all().filter(customer_id = customerId,product_Code=productCode).values('product_Code','customer_id_id','price','products','qty')
            print((queryset))
            #print(dict(queryset))
            # returned=dict(queryset)
            #   sent=Cart.objects.create(queryset) 

        # serializer = OrderSerializer(queryset,many = False)
        except orders.DoesNotExist: 
            return Response({'message': 'Order Detials does not exist','status': 404}, status=status.HTTP_404_NOT_FOUND) 

        # queryset=orders.objects.all().filter(customer_id = customerId,product_Code=productCode).values('product_Code','customer_id')
        # print(queryset)
        # items = <QuerySet [{'product_Code': 2, 'customer_id': 1, 'price': None, 'products': 'lemon', 'qty': 1}]>
        
        
        try :
            for item in queryset:
                newitem = dict(item)
            print(newitem)

            data = Cart(**newitem)
            result=data.save()
            orders.objects.filter(customer_id = customerId,product_Code=productCode).delete()
            # if(result):
            #     obj = get_object_or_404(orders, customer_id = customerId,product_Code=productCode)
            #     obj.delete()
            #     orders.objects.filter(customer_id = customerId).delete()
            #     # querysetdelete=orders.objects.filter(customer_id = customerId,product_Code=productCode).delete()
            #     return Response("success")
            # else:
            #     return Response("something went wrong")
        except :
            return Response({'message': 'Order Detials does not exist','status': 404}, status=status.HTTP_404_NOT_FOUND) 
        


        #blog = Blog.objects.all().values()
        # list=list(Cart.objects.all())
        # product = Cart()
        # # product.<key> = <value>
        # for k, v in queryset.items():
        #     setattr(product, k, v)
        # product.save()
        result = {  
                "status": 201,
                "data": queryset,
                "message": "Order Detials Fetched Successfully",
                
            }
        
        return Response(result)
    # def create(self,**result):
    #     data = get(request,customerId,productCode)
    #     return Response({"data": result})
#for cart get
class cartView(generics.GenericAPIView):
    
    def get(self,request):
        username = self.request.query_params.get('username')
        queryset1 = Cart.objects.select_related('customer_id').filter(customer_id_is_cancel=1)
        # print(queryset1)
        # if username:
            # queryset = Cart.objects.filter(User__user_name =  username)
        #psobjs = Affiliation.objects.filter(ipId=x)
        #queryset = orders.objects.filter(cart1__in=psobjs.values('sessionId'))
        queryset = Cart.objects.filter(is_cancel =  1)
        # else:
            # queryset = Cart.objects.all()
        serializer = CartSerializer(queryset1 , many = True)
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
# @csrf_exempt
# def productsyerapi(request,id=0):
#     if request.method=='GET':
#         # students = products.objects.all()
#         # students_serializer=ProductSerializer(students,many=True)
#         productsapi_data=JSONParser().parse(request)
#         productsapi=products.objects.get(id=productsapi_data['id'])
#         productsapiserializers=ProductSerializer(productsapi)
#         # # result=type(data)
#         # # print(result)
#         return JsonResponse(productsapiserializers.data,safe=False)

#     elif request.method=='POST':
#         productsapi_data=JSONParser().parse(request)
#         productsapiserializers=ProductSerializer(data=productsapi_data)
#         #print(productsapiserializers)
#         if productsapiserializers.is_valid(raise_exception=False):
#             productsapiserializers.save()
#             return JsonResponse("data added succesfully",safe=False)
#         errors = {
#             "message":productsapiserializers.errors,"status":401
#         }
#         return JsonResponse(errors,safe=False)

#for orders.api.
@csrf_exempt
def orderapi(request,id=0):
    if request.method=='GET':
        queryset1 = orders.objects.select_related('customer_id').filter(customer_id_is_cancel=1)
        order_serializer=OrderSerializer(queryset1,many=False)
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

@api_view(['GET'])
def getDetailsBasedOnCaseID(request,customerId,productCode):
    try: 
        lawId = orders.objects.get(customer_id = customerId,product_Code=productCode)
        queryset=orders.objects.all().filter(customer_id = customerId,product_Code=productCode).values('product_Code','customer_id')

        # serializer = OrderSerializer(queryset,many = False)
    except orders.DoesNotExist: 
        return JsonResponse({'message': 'Case Detials does not exist','status': 404}, status=status.HTTP_404_NOT_FOUND) 

    result = {  
                "status": 201,
                "data": queryset,
                "message": "Case Detials Fetched Successfully",
            }
    return JsonResponse(result,safe=False)

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
    token_param_config=openapi.Parameter('image',in_=openapi.IN_QUERY,description='image ',type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
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
class productpost(generics.GenericAPIView):
    # permissions_classes=[permissions.IsAuthenticated]
    serializer_class = ProductSerializer
    parsers_classes=[MultiPartParser,FormParser,FileUploadParser]
    #serializer=ProductSerializer
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


#for prduct order image
class cartpost(generics.GenericAPIView):
    # permissions_classes=[permissions.IsAuthenticated]
    parsers_classes=[MultiPartParser,FormParser]
    serializer=CartSerializer
    def post(self,request,format=None): 
        print(request.data)
        serializer=CartSerializer(data=request.data)
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
               
            })
        return Response({
                "error": serializer.errors,
                "message": "Some thing Went Wrong",
                "status":status.HTTP_400_BAD_REQUEST
            })

class orderupdate(generics.GenericAPIView):
    serializer_class = OrderSerializer
    parsers_classes=[MultiPartParser,FormParser]
    def put(self,request,pk,format=None):
        if request.method=='PUT':
            print(request.data)
            #weightable_data = JSONParser().parse(request)
            orderdata = orders.objects.get(pk=pk)
            ordertable_serializer = OrderSerializer(orderdata,data=request.data,partial=True)
            #is_cancel=False
            # print(ordertable_serializer.data)
            # if is_cancel :
            #     flag=1
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

#delivery quantity get api
class quantityget(APIView):
    
    def get(self,request):
        queryset = QuantityVariant.objects.all()
        serializer = QuantitySerializer(queryset , many = True)
        return Response({'count' : len(serializer.data) ,'data' :serializer.data})

#deliver quantity post api
class quantitypost(generics.GenericAPIView):
    serializer_class = QuantitySerializer
    def post(self, request, *args, **kwargs):
        serializer = QuantitySerializer(data=request.data)
        # law_data = JSONParser().parse(request)
        # serializer=UserRegisterSerializer(data=law_data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "data": serializer.data,
                "message": "orders saved Successfully.",
                "status":status.HTTP_201_CREATED,
                #"token": AuthToken.objects.create(user)[1]
            })
        return Response({
                "error": serializer.errors,
                "message": "Some thing Went Wrong",
                "status":status.HTTP_400_BAD_REQUEST
            })

#delivery address put api
class quantityput(APIView):
    parsers_classes=[MultiPartParser,FormParser]
    def put(self,request,pk,format=None):
        if request.method=='PUT':
            print(request.data)
            #weightable_data = JSONParser().parse(request)
            deliverydata = QuantityVariant.objects.get(id=pk)
            deliverytable_serialzer = QuantitySerializer(deliverydata,data=request.data,partial=True)
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

#delivery address get api
class deliveryaddressget(APIView):
    
    def get(self,request):
        queryset = deliverAddresstable.objects.all()
        serializer = deliveryaddressSerializer(queryset , many = True)
        return Response({'count' : len(serializer.data) ,'data' :serializer.data})

#deliver address post api
class deliveryaddresspost(generics.GenericAPIView):
    serializer_class = deliveryaddressSerializer
    def post(self, request, *args, **kwargs):
        serializer = deliveryaddressSerializer(data=request.data)
        # law_data = JSONParser().parse(request)
        # serializer=UserRegisterSerializer(data=law_data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "data": serializer.data,
                "message": "orders saved Successfully.",
                "status":status.HTTP_201_CREATED,
                #"token": AuthToken.objects.create(user)[1]
            })
        return Response({
                "error": serializer.errors,
                "message": "Some thing Went Wrong",
                "status":status.HTTP_400_BAD_REQUEST
            })
#delivery address put api
class deliveryaddressput(APIView):
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

# class orderdelete(APIView):
#     def delete(self,request,customerId,productCode,*args, **kwargs):
#         try: 
#             orders.objects.filter(customer_id = customerId,product_Code=productCode).delete()
#         except :
#             return Response({'message': 'Order Detials does not exist','status': 404}, status=status.HTTP_404_NOT_FOUND) 

# class DeleteThingView(BaseDetailView):
#     model = orders

#     def delete(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         alldetails=User.objects.delete().filter(customer_id=request.data["customer_id"],product_Code=request.data["product_Code"]).values('product_Code')
#         self.object.delete()
#         response = Response(reverse_lazy("things-list"))
#         response.status_code = 303
#         return response

# class DeleteView(UpdateView, DetailView):
#     template_name = 'sales/edit_sale.html'
#     pk_url_kwarg = 'id'
#     queryset = orders.objects.all()
#     success_url = reverse_lazy('transactions')


# collection = MongoCollection("db_name",
#                              "collection_name",
#                              ["collection_select_key_1", "collection_select_key_2"], 
#                              {filter_key : filter_value})