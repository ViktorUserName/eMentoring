from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from yaml import serialize

from api.models import Course, TeacherSelection, TeacherProfile, StudentProfile
from api.serializers import CourseSerializer, \
    TeacherReadSerializer, UserApiSerializer, RegisterSerializer, StudentReadSerializer, \
    TeacherSelectionCreateSerializer


# =====================USERS VIEWS
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.filter(user__role = 'teacher')
    serializer_class = TeacherReadSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.filter(user__role = 'student')
    serializer_class = StudentReadSerializer

class TeacherSelectionCreateAPIView(generics.CreateAPIView):
    serializer_class = TeacherSelectionCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return TeacherSelection.objects.filter(student=self.request.user.student_profile)
# ====================================
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# class TeacherSelectorViewSet(viewsets.ModelViewSet):
#     queryset = TeacherSelection.objects.all()
#     serializer_class = TeacherSelectionSerializer


# -----USERS/Reg

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
                "detail": f" {user.role} успешно зарегистрирован",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

