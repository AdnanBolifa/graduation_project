from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
import numpy as np

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

class HeartDiseasePredict(APIView):
    def post(self, request):
        serializer = HeartDiseaseSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            # Dummy prediction for testing
            prediction = np.random.choice([0, 1])
            return Response({"prediction": prediction}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class HeartDiseasePredict(APIView):
#     def post(self, request):
#         serializer = HeartDiseaseSerializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.validated_data
#             model = joblib.load('your_model_file_path.pkl')
#             features = np.array([[
#                 data['age'], data['sex'], data['cp'], data['trestbps'],
#                 data['chol'], data['fbs'], data['restecg'], data['thalach'],
#                 data['exang'], data['oldpeak'], data['slope'], data['ca'], data['thal']
#             ]])
#             prediction = model.predict(features)
#             return Response({"prediction": prediction[0]}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)