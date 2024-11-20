from django.urls import include, path
from .views import *

urlpatterns = [
    path('', BucketListView.as_view(), name='bucketlist-list/create'),
    path('<int:pk>/',BucketListView.as_view(), name='bucketlist-detail'),
    #path('goal/<int:pk>/', GoalUpdateView.as_view(), name='goal-detail'),
]