from django.urls import path
from .views import *

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('signup/', UserCreateView.as_view(), name='user_signup'),
    path('predict/', HeartDiseasePredict.as_view(), name='heart_disease_predict'),
    path('refresh_token/', RefreshTokenView.as_view(), name='refresh_token'),
    path('patient_history/', PatientHistoryView.as_view(), name='patient_history'),
    path('feedback/', FeedbackView.as_view(), name='doctor-feedback'),
]
