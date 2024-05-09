from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import numpy as np
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *

class PatientHistoryView(APIView):
    def get(self, request):
        user = request.user
        patient_history = PatientHistory.objects.filter(user=user)
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
                #'user': UserSerializer(user).data
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
            # Save patient history
            PatientHistory.objects.create(user=user, **data)
            # Dummy prediction for testing
            prediction = np.random.choice([0, 1])
            return Response({"prediction": prediction}, status=status.HTTP_200_OK)
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