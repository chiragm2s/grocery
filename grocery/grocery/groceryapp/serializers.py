from rest_framework import serializers
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','is_admin','phno')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password','is_admin','phno')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        phno = data.get("phno")
        if len(str(phno)) != 10:
            raise Exception("Phone number is not valid")
        
        return data


    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'], phno=validated_data.get("phno"),is_admin=validated_data.get("is_admin"))

        return user