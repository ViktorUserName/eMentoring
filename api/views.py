from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Course, TeacherSelection, TeacherProfile
from api.serializers import CourseSerializer, TeacherSelectionSerializer, TeacherCreateSerializer, \
    TeacherReadSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class TeacherSelectorViewSet(viewsets.ModelViewSet):
    queryset = TeacherSelection.objects.all()
    serializer_class = TeacherSelectionSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherReadSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return TeacherCreateSerializer
        return super().get_serializer_class()