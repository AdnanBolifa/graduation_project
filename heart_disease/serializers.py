from rest_framework import serializers
from .models import *

class PatientHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientHistory
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'username': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'sex': {'required': False},
            'age': {'required': False},
            'is_doctor': {'required': False},
            'phone_number': {'required': False},
            'address': {'required': False},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        username = validated_data.get('username')
        if not username:
            # Generate a unique username using the email or another method
            username = validated_data['email'].split('@')[0]
        
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=username,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            sex=validated_data.get('sex', ''),
            age=validated_data.get('age', 0),
            is_doctor=validated_data.get('is_doctor', False),
            phone_number=validated_data.get('phone_number', ''),
            address=validated_data.get('address', '')
        )
        return user


class HypertensionSerializer(serializers.Serializer):
    patientName = serializers.CharField()
    sex = serializers.CharField()
    age = serializers.IntegerField()
    BMI = serializers.FloatField()
    currentSmoker = serializers.IntegerField()
    cigsPerDay = serializers.IntegerField()
    BPMeds = serializers.IntegerField()
    diabetes = serializers.IntegerField()
    totChol = serializers.IntegerField()
    sysBP = serializers.IntegerField()
    diaBP = serializers.IntegerField()
    heartRate = serializers.IntegerField()
    glucose = serializers.IntegerField()

class HeartDiseaseSerializer(serializers.Serializer):
    patientName = serializers.CharField()
    sex = serializers.IntegerField()
    age = serializers.IntegerField()
    BMI = serializers.FloatField()
    currentSmoker = serializers.IntegerField()
    cigsPerDay = serializers.IntegerField()
    BPMeds = serializers.IntegerField()
    prevalentStroke = serializers.IntegerField()
    prevalentHyp = serializers.IntegerField()
    diabetes = serializers.IntegerField()
    totChol = serializers.IntegerField()
    sysBP = serializers.IntegerField()
    diaBP = serializers.IntegerField()
    heartRate = serializers.IntegerField()
    glucose = serializers.IntegerField()

class DiabetesSerializer(serializers.Serializer):
    patientName = serializers.CharField()
    sex = serializers.IntegerField()
    age = serializers.IntegerField()
    BMI = serializers.FloatField()
    Pregnancies = serializers.IntegerField()
    Glucose = serializers.IntegerField()
    BloodPressure = serializers.IntegerField()
    SkinThickness = serializers.IntegerField()
    Insulin = serializers.IntegerField()
    DiabetesPedigreeFunction = serializers.FloatField()

class DiabetesVipSerializer(serializers.Serializer):
    patientName = serializers.CharField()
    sex = serializers.IntegerField()
    age = serializers.IntegerField()
    Urea = serializers.FloatField()
    Cr = serializers.FloatField()
    HbA1c = serializers.FloatField()
    Chol = serializers.FloatField()
    TG = serializers.FloatField()
    HDL = serializers.FloatField()
    LDL = serializers.FloatField()
    VLDL = serializers.FloatField()
    BMI = serializers.FloatField()
    CLASS = serializers.IntegerField(required=False)

class FeedbackSerializer(serializers.Serializer):
    patient_history_id = serializers.IntegerField()
    prediction_result = serializers.BooleanField()