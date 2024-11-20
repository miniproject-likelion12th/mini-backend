from django.urls import path
from .views import SignUpView, LoginView, CustomTokenObtainPairView, LogoutView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='user_signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # 액세스 및 리프레시 토큰 발급
    path('logout/', LogoutView.as_view(), name='user_logout'),
]
