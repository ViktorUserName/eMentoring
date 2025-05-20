from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from yaml import serialize

from api.models import Course, TeacherSelection, TeacherProfile
from api.serializers import CourseSerializer, TeacherSelectionSerializer, TeacherCreateSerializer, \
    TeacherReadSerializer, UserApiSerializer, RegisterSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class TeacherSelectorViewSet(viewsets.ModelViewSet):
    queryset = TeacherSelection.objects.all()
    serializer_class = TeacherSelectionSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.filter(user__role = 'teacher')
    serializer_class = TeacherReadSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return TeacherCreateSerializer
        return super().get_serializer_class()

# -----USERS

class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserApiSerializer(request.user)
        return Response(serializer.data)

class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "detail": f" {request.user.role} успешно зарегистрирован",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

