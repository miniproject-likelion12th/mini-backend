from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import BucketList, Goal
from .serializers import BucketListSerializer, GoalSerializer

# Create your views here.

class BucketListView(APIView):

    #전체 버킷리스트 목록 + 개별 상세 조회
    def get(self, request, pk=None):

        if pk:
            # pk가 주어진 경우, 해당 버킷리스트 반환
            try:
                bucket_list = BucketList.objects.get(pk=pk, user=request.user)
                serializer = BucketListSerializer(bucket_list)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except BucketList.DoesNotExist:
                return Response({"error": "해당 버킷리스트는 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # 필터링 로직 추가
            category = request.query_params.get('category')
            filter_type = request.query_params.get('filter')

            bucket_lists = BucketList.objects.filter(user=request.user)
            
            if category:
                bucket_lists = bucket_lists.filter(category=category)

            if filter_type == 'long_term':
                bucket_lists = bucket_lists.filter(period='long_term')
            elif filter_type == 'short_term':
                bucket_lists = bucket_lists.filter(period='short_term')
            elif filter_type == 'achieved':
                bucket_lists = bucket_lists.filter(is_achieved=True)
            elif filter_type == 'not_achieved':
                bucket_lists = bucket_lists.filter(is_achieved=False)

            serializer = BucketListSerializer(bucket_lists, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    #버킷리스트 생성    
    def post(self, request):
        serializer = BucketListSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 버킷리스트 수정
    def put(self, request, pk):
        try:
            bucket_list = BucketList.objects.get(pk=pk, user=request.user)

            # 버킷 리스트의 내용 수정
            serializer = BucketListSerializer(bucket_list, data=request.data, context={'request': request})
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            # 보낸 형식 오류(필드값의 설정이 잘못되었을 것)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except BucketList.DoesNotExist:
            return Response({"error": "해당 버킷리스트는 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        
    #버킷리스트 달성 여부 상태변화
    def patch(self, request, pk):
        try:
            bucket_list = BucketList.objects.get(pk=pk, user=request.user)

            # is_achieved 값의 상태변화
            is_achieved = request.data.get('is_achieved')

            if is_achieved is not None:
                bucket_list.is_achieved = is_achieved
                bucket_list.save()
                return Response({"is_achieved": bucket_list.is_achieved}, status=status.HTTP_200_OK)
            
            return Response({"error": "is_achieved 필드가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        except BucketList.DoesNotExist:
            return Response({"error": "해당 버킷리스트는 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

    #버킷리스트 삭제    
    def delete(self, request, pk):
        try:
            bucket_list = BucketList.objects.get(pk=pk, user=request.user)
            bucket_list.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BucketList.DoesNotExist:
            return Response({"error": "해당 버킷리스트는 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        

class GoalUpdateView(APIView):
    def patch(self, request, pk):
        goal = Goal.objects.get(pk = pk)
        serializer = GoalSerializer(goal, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
        try:
            goal = Goal.objects.get(pk=pk)
            
            goal.delete()
            
            return Response({"message": "목표가 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        
        except Goal.DoesNotExist:
            return Response({"error": "목표를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
