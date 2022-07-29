from customer.models import UserInfo, OrderTable, PickUpLocation, Cart
from seller.models import Shop, MainFlower, SubFlower, BunchOfFlowers, Deliver

from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.authtoken.models import Token

##################UserInfo 구현###############

class RegisterSerializer(serializers.ModelSerializer): # 회원가입 구현
    password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [validate_password],
    )
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = UserInfo
        fields = ('username', 'password', 'password2', 'name', 'phoneNum', 'address')
        
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password" : "Password fields didn't match."})
        return data
    
    def create(self, validated_data):
        user = UserInfo.objects.create_user(
            username = validated_data['username'],
            name = validated_data['name'],
            phoneNum = validated_data['phoneNum'],
            address = validated_data['address']
        )
        
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user
    
class LoginSerializer(serializers.Serializer): # 로그인 구현
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
        
    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError(
            {"error": "Unable to log in with provided credentials."})
        
class MyPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('name', 'phoneNum', 'address')
        
class MyAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('address')
##############################################


###################CART 구현##################
class CartSerializer(serializers.ModelSerializer):      
    class Meta:
        model = Cart
        fields = ('mainFlower1_ID', 'mainFlower1_amount', 
                  'mainFlower2_ID', 'mainFlower2_amount',
                  'mainFlower3_ID', 'mainFlower3_amount',
                  'subFlower1_ID', 'subFlower1_amount',
                  'subFlower2_ID', 'subFlower2_amount',
                  'subFlower3_ID', 'subFlower3_amount',
                  'bunchOfFlowers1_ID', 'bunchOfFlowers1_amount',
                  'bunchOfFlowers2_ID', 'bunchOfFlowers2_amount'
                  )
#############################################