##################UserInfo 구현###############

from logging import raiseExceptions
from django.contrib.auth.models import AbstractUser
from customer.models import UserInfo
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer, MyPageSerializer, MyAddressSerializer

class RegisterView(generics.CreateAPIView): # 회원가입
    queryset = UserInfo.objects.all()
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    
    
class MyPageAPIView(APIView):
    def get(self, request):
        if request.user:
            myinfo = UserInfo.objects.filter(username = request.user.username)
            serializer = MyPageSerializer(myinfo, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def put(self, request):
        if request.user:
            myinfo = UserInfo.objects.filter(username = request.user.username)
            serializer = MyPageSerializer(myinfo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
class UserDeleteAPIView(APIView):
    def delete(self, request):
        if request.user:
            myinfo = UserInfo.objects.filter(username = request.user.username)
            myinfo.delete()
            return Response("UserInfo successfully deleted!")
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
class UserAddressAPIView(APIView):
    def get(self, request):
        if request.user:
            myinfo = UserInfo.objects.filter(username = request.user.username)
            serializer = MyAddressSerializer(myinfo, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
##############################################


##################Cart 기능 구현###############
from customer.models import Cart
from .serializers import CartSerializer

class CartAPIView(APIView):
    def get(self, request):     #카트에 있는 꽃들 목록 다 가져오기
        if request.user:
            cart = Cart.objects
            serializer = CartSerializer(cart, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request):    #카트 생성
        serializer = CartSerializer(data=request.data)      #Post요청으로 들어온 데이터 시리얼라이저에 넣기
        if serializer.is_valid():       #유효한 데이터라면
            serializer.save(user=request.user)           #역직렬화로 save, 모델시리얼라이저의 기본 create() 함수 동작
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response('안돼~', status=status.HTTP_401_UNAUTHORIZED)
        
class CartAllAPIView(APIView):      #유저의 모든 주문내역 불러오기
    def get(self, request):    
        if request.user:
            cart = Cart.objects.all()
            serializer = CartSerializer(cart, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
#############################################