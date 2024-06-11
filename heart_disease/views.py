import os
import pickle
import joblib
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="X does not have valid feature names")

def load_model(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)
    
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, '..', 'models', 'model.pkl')


LR_model = load_model(model_path)

class PatientHistoryView(APIView):
    def get(self, request):
        user = request.user
        patient_history = PatientHistory.objects.filter(user=user).order_by('-created_at')
        serializer = PatientHistorySerializer(patient_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = CustomUser.objects.filter(email=email).first()
        if user is not None and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class HeartDiseasePredict(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = HeartDiseaseSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = request.user  # Get the current user

            features = [
                data['sex'], data['age'], data['currentSmoker'], data['cigsPerDay'], 
                data['BPMeds'], data['prevalentStroke'], data['prevalentHyp'], 
                data['diabetes'], data['totChol'], data['sysBP'], data['diaBP'], 
                data['BMI'], data['heartRate'], data['glucose']
            ]

            user_data = pd.DataFrame([features])

            try:
                prediction = LR_model.predict(user_data)
                probability = LR_model.predict_proba(user_data)

                result = {
                    "prediction": int(prediction[0]),
                    "probability_positive": probability[0][1] * 100,
                    "probability_negative": probability[0][0] * 100
                }
                data['TenYearCHD'] = prediction[0]
                PatientHistory.objects.create(user=user, **data)
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=400)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({"access_token": access_token}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
class FeedbackView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                patient_history = PatientHistory.objects.get(id=data['patient_history_id'])
                patient_history.doctor_feedback = data['prediction_result']
                patient_history.save()
                return Response({"message": "Feedback saved successfully."})
            except PatientHistory.DoesNotExist:
                return Response({"error": "Patient history not found."}, status=404)
        return Response(serializer.errors, status=400)