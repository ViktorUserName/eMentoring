from rest_framework.routers import DefaultRouter
from django.urls import path, include

from api.utils.router import CustomRouter
from api.views import CourseViewSet, TeacherViewSet, UserAPIView, UserRegisterView, \
    StudentViewSet, TeacherSelectionCreateAPIView

router = CustomRouter(custom_routes={
    'user-info': 'user-info',
    'sign-in': 'sign-in',
    'teacher-selection': 'teacher-selection',
})
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'teachers', TeacherViewSet, basename='teachers')
# router.register(r'select', TeacherSelectorViewSet, basename='select')
router.register(r'student', StudentViewSet, basename='student')


urlpatterns = [
    path('', include(router.urls)),
    path(r'user-info', UserAPIView.as_view(), name='user-info'),
    path(r'sign-in', UserRegisterView.as_view(), name='sign-in'),
    path(r'teacher-selection', TeacherSelectionCreateAPIView.as_view(), name='teacher-selection'),

]
