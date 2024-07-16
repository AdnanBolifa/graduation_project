from rest_framework import serializers
from .models import *

class PatientHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientHistory
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'sex', 'age', 'is_doctor', 'phone_number', 'address']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            sex=validated_data.get('sex', ''),
            age=validated_data.get('age', 0),
            is_doctor=validated_data.get('is_doctor', False),
            phone_number=validated_data.get('phone_number', ''),
            address=validated_data.get('address', '')
        )
        return user



class HeartDiseaseSerializer(serializers.Serializer):
    patientName = serializers.CharField()
    sex = serializers.IntegerField()
    age = serializers.IntegerField()
    currentSmoker = serializers.IntegerField()
    cigsPerDay = serializers.IntegerField()
    BPMeds = serializers.IntegerField()
    prevalentStroke = serializers.IntegerField()
    prevalentHyp = serializers.IntegerField()
    diabetes = serializers.IntegerField()
    totChol = serializers.IntegerField()
    sysBP = serializers.IntegerField()
    diaBP = serializers.IntegerField()
    BMI = serializers.FloatField()
    heartRate = serializers.IntegerField()
    glucose = serializers.IntegerField()
    prediction_result = models.BooleanField()

from rest_framework import serializers

class DiabetesPredictionSerializer(serializers.Serializer):
    Gender = serializers.IntegerField()
    AGE = serializers.IntegerField()
    Urea = serializers.FloatField()
    Cr = serializers.FloatField()
    HbA1c = serializers.FloatField()
    Chol = serializers.FloatField()
    TG = serializers.FloatField()
    HDL = serializers.FloatField()
    LDL = serializers.FloatField()
    VLDL = serializers.FloatField()
    BMI = serializers.FloatField()


class FeedbackSerializer(serializers.Serializer):
    patient_history_id = serializers.IntegerField()
    prediction_result = serializers.BooleanField()