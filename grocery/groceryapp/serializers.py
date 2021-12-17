from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from django.contrib.auth import authenticate #for authentication and phone otp
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import *
User = get_user_model()
from drf_extra_fields.fields import Base64FileField, Base64ImageField
import base64

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','is_admin','phno', 'first_login')
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email','is_admin','phno', 'first_login')




#its like registration serializer
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'password')
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
#         return user

# # Register Serializer
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username',  'password','is_admin','phone')
#         extra_kwargs = {'password': {'write_only': True}}

#     def validate(self, data):
#         phno = data.get("phone")
#         if len(str(phno)) != 10:
#             raise Exception("Phone number is not valid")
        
#         return data


#     def create(self, validated_data):
#         print(validated_data)
#         user = User.objects.create_user(username=validated_data['username'],email= validated_data['email'], password=validated_data['password'], phno=validated_data.get("phone"),is_admin=validated_data.get("is_admin"))

#         return user


# # User serializer
# class UserRegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'password','is_admin','phone','name')
#         extra_kwargs = {'password': {'write_only': True}}
    
#     def validate(self, attrs):
#         # print("data")
        
#         username = attrs.get('username','')
#         phone = attrs.get('phone','')
#         # password = attrs.get('password','')
#         # print(password)
#         if User.objects.filter(username=username).exists():
#             raise serializers.ValidationError(
#                 {'username':{'Email Already in use'}})
#         elif len(str(phone)) != 10:
#             raise serializers.ValidationError(
#                 {'phone':'Phone Number must be 10 Digits'})
#         return super().validate(attrs)

#     def create(self, validated_data):
#         print(validated_data)
#         user = User.objects.create_user(username= validated_data['username'], password=validated_data['password'], phone=validated_data.get("phone"),is_admin=validated_data.get("is_admin"))
#         return user


# User serializer
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone','name','is_admin','is_customer','is_deliveryboy', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

##Login Serializer
class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            
            if User.objects.filter(email=email).exists():
                user = authenticate(request=self.context.get('request'),
                                    email=email, password=password)
                print(password)
                
            else:
                msg = {'detail': 'Email ID is not registered.',
                       'register': False,"status":404}
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'detail': 'Unable to log in with provided credentials.', 'register': True,"status":404}
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include "Email ID" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        
        return attrs

class QuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuantityVariant
        fields = '__all__' 
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class deliveryaddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = deliverAddresstable
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__' 

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = delivery
        fields = '__all__' 

class DeliveryAssignedSerializer(serializers.ModelSerializer):
    class Meta:
        model = delivery_assigned
        fields = '__all__' 
    

class ProductSerializer(serializers.ModelSerializer):
    #category = CategorySerializer()
    #quantity_type = QuantitySerializer()
    #image = Base64ImageField()
    class Meta:
        model = products
        fields = ('__all__')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = orders
        fields = '__all__'

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = delivery
        fields = '__all__'


# ##Login Serializer
# class LoginUserSerializer(serializers.Serializer):
#     email = serializers.CharField()
#     password = serializers.CharField(
#         style={'input_type': 'password'}, trim_whitespace=False)
    

#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
#         # email = attrs.get('email')
#         # print(email)
#         # if not password:
#         #         msg = {'detail': 'email number is not registered.',
#         #                'register': False,"status":404}
#         #         raise serializers.ValidationError(msg) 
#         if email and password:
            
#             if User.objects.filter(username=email).exists():
#                 user = authenticate(request=self.context.get('request'),
#                                     username=email, password=password)
                
#             else:
#                 msg = {'detail': 'username is not registered.',
#                        'register': False,"status":404}
#                 raise serializers.ValidationError(msg)

#             if not user:
#                 msg = {
#                     'detail': 'Unable to log in with provided credentials.', 'register': True,"status":404}
#                 raise serializers.ValidationError(msg, code='authorization')

#         else:
#             msg = 'Must include "username" and "password".'
#             raise serializers.ValidationError(msg, code='authorization')

#         attrs['user'] = user
        
#         return attrs

#for change of password
class ChangePasswordSerializer(serializers.Serializer):
    """
    Used for both password change (Login required) and 
    password reset(No login required but otp required)
    not using modelserializer as this serializer will be used for for two apis
    """

    password_1 = serializers.CharField(required=True)
    # password_1 can be old password or new password
    password_2 = serializers.CharField(required=True)
    # password_2 can be new password or confirm password according to apiview

#for forgot of password
class ForgetPasswordSerializer(serializers.Serializer):
    """
    Used for resetting password who forget their password via otp varification
    """
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)