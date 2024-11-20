from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, logout as auth_logout
from .models import User
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@permission_classes([AllowAny])
class SignUpView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        password2 = request.data.get('password2')
        email = request.data.get('email')

        # 비밀번호 일치 확인
        if password != password2:
            return Response({"message": "입력한 비밀번호가 다릅니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 비밀번호 유효성 검사
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"message": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        # serializer로 유효성 검사 후 데이터 전달
        data = {
            "username": username,
            "email": email,
            "password": password,
        }
        serializer = UserSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(password)  # 비밀번호 암호화 저장
            user.save()

            return Response({"user_id": user.user_id, "message": "회원가입에 성공하였습니다."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
# 로그인 뷰
@permission_classes([AllowAny])
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            return Response({
                "user_id": user.user_id,
                "username": user.username,
                "message": "로그인 성공"
            }, status=status.HTTP_200_OK)

        return Response({"message": "이메일 또는 비밀번호가 잘못되었습니다."}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Authorization 헤더에서 리프레시 토큰 추출
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()  # 토큰을 블랙리스트에 추가

            return Response({"message": "로그아웃 성공"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "유효하지 않은 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)