from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='user_signup'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('predict/', HeartDiseasePredict.as_view(), name='heart_disease_predict'),
    path('refresh_token/', RefreshTokenView.as_view(), name='refresh_token'),
]
