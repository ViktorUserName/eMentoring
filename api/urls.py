from rest_framework.routers import DefaultRouter
from django.urls import path, include

from api.views import CourseViewSet, TeacherSelectorViewSet, TeacherViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'teachers', TeacherViewSet, basename='teachers')

router.register(r'select', TeacherSelectorViewSet, basename='select')



urlpatterns = [
    path('', include(router.urls)),
]