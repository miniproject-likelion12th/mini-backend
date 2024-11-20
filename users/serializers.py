from rest_framework.serializers import ModelSerializer
from .models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # 사용자 정보 추가
        data.update({
            'user_id': self.user.user_id,
            'username': self.user.username,
            'email': self.user.email,
        })

        return data

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'password']  
        extra_kwargs = {'password': {'write_only': True}}  # 비밀번호는 쓰기 전용으로 설정

    # 회원가입
    def create(self, validated_data):
        user = super().create(validated_data)
        password = validated_data.get('password')
        user.set_password(password)
        user.save()
        return user

    # 로그인 시 비밀번호 갱신 (만약 업데이트가 필요한 경우)
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        password = validated_data.get('password')
        if password:
            user.set_password(password)
            user.save()
        return user
    