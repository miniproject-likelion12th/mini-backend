from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class BucketList(models.Model):
    PERIOD_CHOICES = [
        ('long_term', 'Long Term'),
        ('short_term', 'Short Term'),
    ]

    CATEGORY_CHOICES = [
        ('travel', '여행'),
        ('hobby_culture', '취미/문화'),
        ('health_exercise', '건강/운동'),
        ('spending_saving_donating', '소비/저축/기부'),
        ('self_development', '자기계발'),
        ('others', '기타'),
        ('career', '커리어'),
        ('family_friends', '가족/친구'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bucket_lists')
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    motive = models.TextField()
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    is_achieved = models.BooleanField(default=False)
    duration_years = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}. Title: {self.title}"

class Goal(models.Model):
    bucket_list = models.ForeignKey(BucketList, on_delete=models.CASCADE, related_name = 'goals')
    year = models.PositiveIntegerField(null=True, blank=True)#장기
    month = models.PositiveIntegerField(null=True, blank=True)#단기
    content = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"Bucketlist: {self.bucket_list.id} , Goal : {self.id} "

