from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
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
