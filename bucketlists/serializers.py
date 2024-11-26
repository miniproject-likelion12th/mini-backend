from rest_framework import serializers
from .models import *

class GoalSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False) 
    #id를 입력받을 수 있는 필드로 클라이언트가 보낼 수 있는 필드로 수정! 이걸 토대로 goal의 갱신 관리!

    class Meta:
        model = Goal
        fields = ['id', 'year', 'month', 'content', 'is_done']



class BucketListSerializer(serializers.ModelSerializer):
    goals = GoalSerializer(many = True, required=False)

    class Meta:
        model = BucketList
        fields = ['id', 'title', 'category', 'motive', 'period', 'duration_years','is_achieved', 'goals']

    def create(self, validated_data):
        goals_data = validated_data.pop('goals', [])  # goals 데이터를 분리
        user = self.context['request'].user  # 요청에서 사용자 정보를 가져옴
        bucketlist = BucketList.objects.create(user=user, **validated_data)

        for goal_data in goals_data:
            Goal.objects.create(bucket_list=bucketlist, **goal_data) # Goal 생성

        return bucketlist
    
    def update(self, instance, validated_data):
        goals_data = validated_data.pop('goals', [])
        
        #print("validated_data:", validated_data)
        #print("goals_data:", goals_data)

        # BucketList 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        current_goals = {goal.id: goal for goal in instance.goals.all()}
        #print("현재 goals:", current_goals.keys())

        processed_ids = set()
        for goal_data in goals_data:
            goal_id = goal_data.get('id')
            #print(f"처리 중인 goal_data: {goal_data}")
            #print(f"처리 중인 goal_id: {goal_id}")

            if goal_id and goal_id in current_goals:
                goal = current_goals[goal_id]
                for attr, value in goal_data.items():
                    setattr(goal, attr, value)
                goal.save()
                processed_ids.add(goal_id)
                #print(f"수정된 goal_id: {goal_id}")
            elif not goal_id:
                new_goal = Goal.objects.create(bucket_list=instance, **goal_data)
                processed_ids.add(new_goal.id)
                #print(f"생성된 goal_id: {new_goal.id}")

        to_delete_ids = set(current_goals.keys()) - processed_ids
        #print("삭제될 goals:", to_delete_ids)
        for goal_id in to_delete_ids:
            current_goals[goal_id].delete()

        return instance
    #어라라.. validated_data에서 왜 goalid가 누락되는거지


    def to_representation(self, instance):
        # 기본 직렬화 데이터를 가져옴
        representation = super().to_representation(instance)

        # 'goals'가 있을 경우, goals를 'year'와 'month' 기준으로 정렬
        if 'goals' in representation:
            # GoalSerializer로 직렬화된 목표들을 year, month 순으로 정렬 (None 값을 마지막으로 처리)
            representation['goals'] = sorted(representation['goals'], key=lambda x: (
                x.get('year') is None,  # year 값이 None인 경우 마지막에 위치
                x.get('month') is None, # month 값이 None인 경우 마지막에 위치
                x.get('year', 0),       # year 값으로 먼저 정렬 (None이면 0으로 처리)
                x.get('month', 0)       # month 값으로 두 번째로 정렬 (None이면 0으로 처리)
            ))

        return representation
