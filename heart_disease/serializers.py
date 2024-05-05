from rest_framework import serializers
from .models import CustomUser

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
    age = serializers.IntegerField()
    sex = serializers.IntegerField()
    cp = serializers.IntegerField()
    trestbps = serializers.IntegerField()
    chol = serializers.IntegerField()
    fbs = serializers.IntegerField()
    restecg = serializers.IntegerField()
    thalach = serializers.IntegerField()
    exang = serializers.IntegerField()
    oldpeak = serializers.FloatField()
    slope = serializers.IntegerField()
    ca = serializers.IntegerField()
    thal = serializers.IntegerField()
