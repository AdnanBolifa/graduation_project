from django.urls import path
from .views import UserCreateView, UserLoginView, HeartDiseasePredict

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='user_signup'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('predict/', HeartDiseasePredict.as_view(), name='heart_disease_predict'),
]
