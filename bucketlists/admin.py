from django.contrib import admin
from .models import BucketList, Goal

# Register your models here.

class GoalInline(admin.TabularInline): 
    model = Goal
    extra = 1  #기본 설정으로 한 개의 Goal 폼을 추가하도록 설정

# BucketList 모델을 관리할 수 있도록 설정
class BucketListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'period', 'is_achieved', 'user')  
    search_fields = ('title', 'category') 
    list_filter = ('category', 'period', 'is_achieved')  
    inlines = [GoalInline]  # BucketList와 연결된 Goal을 관리할 수 있도록 설정

# Goal 모델을 관리할 수 있도록 설정
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'bucket_list', 'content', 'year', 'month', 'is_done')  
    search_fields = ('content',)  
    list_filter = ('is_done', 'year', 'month')  


admin.site.register(BucketList, BucketListAdmin)
admin.site.register(Goal, GoalAdmin)