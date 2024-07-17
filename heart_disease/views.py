import logging
import os
import pickle
import warnings

import numpy as np
import pandas as pd
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *
from .serializers import *

warnings.filterwarnings("ignore", category=UserWarning, message="X does not have valid feature names")

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

class PredictionView(APIView):
    permission_classes = [IsAuthenticated]

    @classmethod
    def prepare_heart_data(cls, data):
        features = [
            data['sex'], data['age'], data['currentSmoker'], data['cigsPerDay'],
            data['BPMeds'], data['prevalentStroke'], data['prevalentHyp'],
            data['diabetes'], data['totChol'], data['sysBP'], data['diaBP'],
            data['BMI'], data['heartRate'], data['glucose']
        ]
        columns = ['sex', 'age', 'currentSmoker', 'cigsPerDay', 'BPMeds', 'prevalentStroke', 'prevalentHyp',
                   'diabetes', 'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose']
        user_data = pd.DataFrame([features], columns=columns)
        user_data.rename(columns={'sex': 'male'}, inplace=True)
        return user_data

    @classmethod
    def prepare_diabetes_vip_data(cls, data):
        features = [
            data['sex'], data['age'], data['Urea'], data['Cr'],
            data['HbA1c'], data['Chol'], data['TG'], data['HDL'],
            data['LDL'], data['VLDL'], data['BMI']
        ]
        columns = ['sex', 'age', 'Urea', 'Cr', 'HbA1c', 'Chol', 'TG', 'HDL', 'LDL', 'VLDL', 'BMI']
        user_data = pd.DataFrame([features], columns=columns)
        user_data.rename(columns={'sex': 'Gender'}, inplace=True)
        user_data.rename(columns={'age': 'AGE'}, inplace=True)
        return user_data

    @staticmethod
    def prepare_diabetes_data(data):
        features = [
            data['Pregnancies'], data['Glucose'], data['BloodPressure'], data['SkinThickness'],
            data['Insulin'], data['BMI'], data['DiabetesPedigreeFunction'], data['age']
        ]
        columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 
                   'DiabetesPedigreeFunction', 'age']
        user_data = pd.DataFrame([features], columns=columns)
        user_data.rename(columns={'age': 'Age'}, inplace=True)
        return user_data

    @classmethod
    def prepare_hypertension_data(cls, data):
        features = [
            data['sex'], data['age'], data['currentSmoker'], data['cigsPerDay'],
            data['BPMeds'], data['diabetes'], data['totChol'], data['sysBP'], data['diaBP'],
            data['BMI'], data['heartRate'], data['glucose']
        ]
        columns = ['sex', 'age', 'currentSmoker', 'cigsPerDay', 'BPMeds', 
                   'diabetes', 'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose']
        user_data = pd.DataFrame([features], columns=columns)
        user_data.rename(columns={'sex': 'male'}, inplace=True)
        return user_data

    @classmethod
    def prepare_patient_history_data(cls, data, prediction_type, user):
        print('data', data)
        print('age', data.get('age'))
        patient_history_data = {
            'user': user,
            'patientName': data.get('patientName'),
            'prediction_type': prediction_type,
            'sex': data.get('sex'),
            'age': data.get('age'),
            'BMI': data.get('BMI'),
            'Prediction': data.get('Prediction'),
        }

        if prediction_type == 'heart':
            patient_history_data.update({
                'currentSmoker': data.get('currentSmoker'),
                'cigsPerDay': data.get('cigsPerDay'),
                'BPMeds': data.get('BPMeds'),
                'prevalentStroke': data.get('prevalentStroke'),
                'prevalentHyp': data.get('prevalentHyp'),
                'diabetes': data.get('diabetes'),
                'totChol': data.get('totChol'),
                'sysBP': data.get('sysBP'),
                'diaBP': data.get('diaBP'),
                'heartRate': data.get('heartRate'),
                'glucose': data.get('glucose'),
            })
        elif prediction_type == 'diabetes_vip':
            patient_history_data.update({
                'Urea': data.get('Urea'),
                'Cr': data.get('Cr'),
                'HbA1c': data.get('HbA1c'),
                'Chol': data.get('Chol'),
                'TG': data.get('TG'),
                'HDL': data.get('HDL'),
                'LDL': data.get('LDL'),
                'VLDL': data.get('VLDL'),
            })
        elif prediction_type == 'hypertension':
            patient_history_data.update({
                'currentSmoker': data.get('currentSmoker'),
                'cigsPerDay': data.get('cigsPerDay'),
                'BPMeds': data.get('BPMeds'),
                'diabetes': data.get('diabetes'),
                'totChol': data.get('totChol'),
                'sysBP': data.get('sysBP'),
                'diaBP': data.get('diaBP'),
                'heartRate': data.get('heartRate'),
                'glucose': data.get('glucose'),
            })
        elif prediction_type == 'diabetes':
            patient_history_data.update({
                'Pregnancies': data.get('Pregnancies'),
                'glucose': data.get('Glucose'),
                'BloodPressure': data.get('BloodPressure'),
                'SkinThickness': data.get('SkinThickness'),
                'Insulin': data.get('Insulin'),
                'BMI': data.get('BMI'),
                'DiabetesPedigreeFunction': data.get('DiabetesPedigreeFunction'),
            })
        else:
            raise ValueError("Invalid prediction type")
        return patient_history_data

    @classmethod
    def load_model(cls, filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)

    @classmethod
    def get_model(cls, model_type):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_paths = {
            'heart': os.path.join(current_dir, '..', 'models', 'heart.pkl'),
            'diabetes': os.path.join(current_dir, '..', 'models', 'diabetes_model.pkl'),
            'diabetes_vip': os.path.join(current_dir, '..', 'models', 'diabetes_vip_model.pkl'),
            'hypertension': os.path.join(current_dir, '..', 'models', 'hypertension.pkl')
        }
        model_path = model_paths.get(model_type)
        if model_path:
            return cls.load_model(model_path)
        else:
            raise ValueError("Invalid prediction type")

    def post(self, request):
        prediction_type = request.data.get('prediction_type')

        if prediction_type == 'heart':
            serializer = HeartDiseaseSerializer(data=request.data)
            prepare_data = self.prepare_heart_data
        elif prediction_type == 'diabetes':
            serializer = DiabetesSerializer(data=request.data)
            prepare_data = self.prepare_diabetes_data
        elif prediction_type == 'diabetes_vip':
            serializer = DiabetesVipSerializer(data=request.data)
            prepare_data = self.prepare_diabetes_vip_data
        elif prediction_type == 'hypertension':
            serializer = HypertensionSerializer(data=request.data)
            prepare_data = self.prepare_hypertension_data
        else:
            return Response({"error": "Invalid prediction type"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            data = serializer.validated_data
            user = request.user
            user_data = prepare_data(data)
            
            if not isinstance(user_data, pd.DataFrame):
                return Response({"error": "Invalid data format for prediction"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            try:
                model = self.get_model(prediction_type)
                prediction = model.predict(user_data)
                probability = model.predict_proba(user_data)

                result = {
                    "prediction": int(prediction[0]),
                    "probability_positive": probability[0][1] * 100,
                    "probability_negative": probability[0][0] * 100
                }
                data['Prediction'] = prediction[0]
                patient_history_data = self.prepare_patient_history_data(data, prediction_type, user)
                print('patient_history_data', patient_history_data)
                PatientHistory.objects.create(**patient_history_data)

                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"try error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
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